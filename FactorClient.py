#! /usr/bin/env python

import argparse
from twisted.internet import reactor,protocol,defer
from twisted.protocols import basic
import datetime
import pickle
import NetJob
import math
import md5

#Factor Client Protocol
class FCProtocol(basic.LineReceiver):

    def __init__(self,factory,state='INI'):
        self.state=state
        self.factory=factory

    def connectionMade(self):
        if arguments.verbose: 
            print "[%s] Connection made with %s:%s, protocol state: %s" % (tstamp(),self.transport.getPeer().host,self.transport.getPeer().port,self.state)

    def lineReceived(self,line):
        proto_msg=line.split(':',1)
        if len(proto_msg) == 2: 
            self.speak_proto(proto_msg)
        else:
            print "Received unknown message : %s" % line
            self.transport.loseConnection()

    def connectionLost(self,reason):
        print "[%s] Conection closed with %s:%s with message: %s" % (tstamp(),self.transport.getPeer().host,self.transport.getPeer().port,reason.getErrorMessage())
        if not self.state in ['ASGJOB','ACKRECV']: #If we don't have the job assigment yet, then stop the reactor
            print "Stoping reactor"
            reactor.stop()

    #Parameters:  message.- The two elements list with the protocol message received from
    #                       the server, the first element is the protocol command and the
    #                       second the protocol additional info
    def speak_proto(self,message):
        '''Manages the protocol conversation with the server'''
        if self.state=='INI' and message[0].strip() == 'READY TO ACCEPT REQUESTS':
            self.factory.getID(self.transport.getHost().host)
            if arguments.verbose: print "[%s] Sending register request with ID: %s..." % (tstamp(),self.factory.clientID[:7])
            self.transport.write("REGISTER:%s\r\n" % self.factory.clientID)
            self.state='REG'
        elif self.state=='REG' and message[0].strip() =='REGISTERED':
            self.request=NetJob.NetJob(self.factory.clientID,'REQUEST')
            self.pickled_request=pickle.dumps(self.request,pickle.HIGHEST_PROTOCOL)
            if arguments.verbose: print "[%s] Registered, sending job request: %s" % (tstamp(),self.request)
            self.transport.write("REQUEST JOB:%s\r\n" % self.pickled_request)
            self.state='REQJOB'
        elif self.state=='REQJOB':
            if message[0].strip() =='JOB SEGMENT':
                self.factory.job_segment=pickle.loads(message[1].strip())
                if self.factory.job_segment.is_response():
                    if arguments.verbose: print "[%s] Receiving job segment: %s" % (tstamp(),self.factory.job_segment)
                    self.state='ASGJOB'
                    d=self.factory.factor(self.factory.job_segment)
                    d.addCallback(self.factory.send_results)
                    d.addErrback(self.factory.factoring_err)
                    self.transport.loseConnection()
                else:
                    print "[%s] Expecting a RESPONSE object, got: %s" % self.factory.job_segment
                    reactor.stop()
            elif message[0].strip() == 'REQUEST TIMEOUT':
                print "[%s] Request time out: %s" % (tstamp(),message[1].strip())
                print "[%s] Resending job request" % tstamp()
                self.transport.write("REQUEST JOB:%s\r\n" %self.pickled_request)
            else: #@Repeated code
                print "[%s] Expecting a RESPONSE object, got: %s" % self.factory.job_segment
                reactor.stop()
        elif self.state == 'WAITACK': #We are wating for an ACK
            if message[0].strip() == 'JOB SEGMENT':
                ack_job_segment=pickle.loads(message[1].strip())
                if ack_job_segment.is_ack() and ack_job_segment.worker_ID == self.factory.job_segment.worker_ID:
                    print "[%s] ACK received: %s" % (tstamp(),ack_job_segment)
                    self.state='ACKRECV' 
                    self.factory.new_connection()
                    self.transport.loseConnection()
                else:
                    print "[%s] Expecting an ACK object, got: %s" % (tstamp(),ack_job_segment)
                    reactor.stop()
            elif message[0].strip() == 'REQUEST TIMEOUT':
                print "[%s] %s. Sending results again. Waiting for ACK" % (tstamp(),message[1].strip())
                self.transport.write("SEND RESULTS:%s\r\n" % pickle.dumps(self.factory.job_segment,pickle.HIGHEST_PROTOCOL ))
        elif self.state =='ASGJOB' and message[0].strip() == 'READY TO ACCEPT REQUESTS':
            self.transport.write("SEND RESULTS:%s\r\n" % pickle.dumps(self.factory.job_segment,pickle.HIGHEST_PROTOCOL ))
            self.state='WAITACK'
            print "[%s] Results sent, waiting for ACK" % tstamp()
        else:
            print "Bad protocol, current state: %s message received: %s" % (self.state,message[0])





#Factor Client Factory
class FCFactory(protocol.ClientFactory):

    #Identitification for this client, assigned by the server
    clientID=None
    #NetJob object containing the factoring job to solve, only one is available per factory
    job_segment=None

    def getID(self,address):
        reg_time=datetime.datetime.now()
        self.clientID=md5.new(str(address) + str(reg_time)).hexdigest()

    def buildProtocol(self,addr):
        return FCProtocol(self,state='ASGJOB') if self.job_segment and self.job_segment.results is not None else FCProtocol(self)

    def clientConnectionFailed(self,connector,reason):
        Address=connector.getDestination()
        print "Could not connect to host %s port %d, due to %s" % (Address.host,Address.port,reason)
        reactor.stop()

    #Parameters: compnum.- An integer to factorize
    #           gerbasio.- A deferred object to call when finished
    #           candidate.- The first candidate to start looking for factors
    #           last_candidate.- The last candidate to try
    #Return:  The list of factors found, with duplacates
    def factorize_with_limits(self,compnum,gerbasio,candidate=2,last_candidate=2):
        '''Multiprocess function used to factor a number, it will look for factors inside
        a defined segment, between an initial and a final possible candidates.'''

        #This data structure is used to adjust the initial candidate, and select the correct
        #increment dictionary
        cand_adj_increments= {0:('1',[2,4,2,2]),
                              1:('1',[2,4,2,2]),
                              2:('3',[4,2,2,2]),
                              3:('3',[4,2,2,2]),
                              4:('7',[2,2,2,4]),
                              5:('7',[2,2,2,4]),
                              6:('7',[2,2,2,4]),
                              7:('7',[2,2,2,4]),
                              8:('9',[2,2,4,2]),
                              9:('9',[2,2,4,2])}

        own_results=list() #List to store the factors found in this segment
        max_candidate=min(last_candidate,int(math.ceil(math.sqrt(compnum)))) #Square root of the number to factor
    #Place the candidate in the correct position; if the candidate ends in 7, 9, 1 or 3 do nothing
        if candidate > 5:
            updated_last_figure ,increment = cand_adj_increments[candidate%10]
            candidate =int(str(candidate)[:-1]+updated_last_figure) #Add the new ending
        else: #candidate is 2, 3, 4 or 5
            increment=cand_adj_increments[7][1] #The 7 increment list is used
        #signal.signal(signal.SIGUSR1,signal_show_current_status) #Sets the handler for the signal SIGUSR1
        if candidate == 2: #This condition is here because the initial value of candidate may be different from 2
            while compnum%candidate == 0:  #Candidate = 2, consider it as a special case
                compnum,max_candidate=self.update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += 1 #Now candidate equals 3
        if candidate == 3: #This condition is here because the initial value of candidate may be different from 2
            while compnum%candidate == 0:
                compnum,max_candidate=self.update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += 2 #Now candidate equals 5
        if candidate == 4: candidate = 5 #Upgrade to the next meaninful candidate
        if candidate == 5: #This condition is here because the initial value of candidate may be different from 2
            while compnum%candidate == 0:
                compnum,max_candidate=self.update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += 2 #Now candidate equals 7
    #----MAIN LOOP----
        while candidate <= max_candidate:
            while compnum%candidate == 0:
                compnum,max_candidate=self.update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += increment[0] #This increment depends on the incremnet list selected bejore
            while compnum%candidate == 0:
                compnum,max_candidate=self.update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += increment[1] #This increment depends on the incremnet list selected bejore
            while compnum%candidate == 0:
                compnum,max_candidate=self.update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += increment[2] #This increment depends on the incremnet list selected bejore
            while compnum%candidate == 0:
                compnum,max_candidate=self.update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += increment[3] #This increment depends on the incremnet list selected bejore
        if compnum != 1: own_results.append(compnum)
        print "[%s] factors found: %s" % (tstamp(),own_results)
        gerbasio.callback(own_results)

    #Parameters: compnum.- An integer to factorize
    #            own_results.- list to store the factors found during the execution of the function.
    #           candidate.- The first candidate to start looking for factors
    #           last_candidate.- The last candidate to try
    #           max_candidate.- The maximun value a candidate can get to look for factors
    #Returns: The updated values of compnum and max_candidate. The own_results is also
    #         updated, but this is done in-place
    def update_resnum(self,compnum,own_results,candidate,last_candidate,max_candidate):
        '''This function is called when a new factor is found. Adds the factor found to the
        results list; updates the number to factor, dividing it by the factor found; and
        updates the maximun candidate'''
        own_results.append(candidate)
        compnum /= candidate
        max_candidate=min(last_candidate,int(math.ceil(math.sqrt(compnum)))) #Square root of the number to factor
        return (compnum,max_candidate)

    
    #Parameters:  The job segment to solve
    def factor(self,job_segment):
        '''Waits a moment before launching the factoring function, so the connection can be
        cleanly closed '''
        d=defer.Deferred()
        reactor.callLater(1,self.factorize_with_limits,job_segment.num,d,job_segment.segment[0],job_segment.segment[1])
        return d

    def send_results(self,own_results):
        '''Adds the results from factoring to the NetJob object, then opens a connection
        with the server, what triggers the sending of the result based on the state of
        the protocol '''
        self.job_segment.add_results(own_results)
        if arguments.verbose: print "[%s] Sending job results: %s" % (tstamp(),self.job_segment)
        reactor.connectTCP(arguments.host,arguments.port,self)

    def factoring_err(self,err):
        err.printBriefTraceback()
        reactor.stop()

    def new_connection(self):
        self.job_segment=None
        reactor.connectTCP(arguments.host,arguments.port,self)

#Parameters: none
#Return value: the arguments found in the command line
def parse_arguments():
    '''Parses the command line arguments'''
    parser=argparse.ArgumentParser(description="Find the prime factors of an integer numberi within a segments, all supplied by a server")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("host",default='localhost', help="Host name or IP to connect to")
    parser.add_argument("port", help="Server port to connect to", type=int)
    return parser.parse_args()

def tstamp():
    ts=datetime.datetime.now()
    return "%d:%d:%d.%d" % (ts.hour,ts.minute,ts.second,ts.microsecond/1000)

def main():
    reactor.connectTCP(arguments.host,arguments.port,FCFactory())
    reactor.run()

if __name__ == '__main__':
    arguments=parse_arguments()
    main()

