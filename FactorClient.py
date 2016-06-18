#! /usr/bin/env python

import argparse
from twisted.internet import reactor,protocol
from twisted.protocols import basic
import datetime
import pickle
import NetJob
import math

#Factor Client Protocol
class FCProtocol(basic.LineReceiver):

    def __init__(self,factory):
        self.state='INI'
        self.factory=factory

    def connectionMade(self):
        if arguments.verbose: print ("Connection made")

    def lineReceived(self,line):
        proto_msg=line.split(':',1)
        if len(proto_msg) == 2: 
            self.speak_proto(proto_msg)
        else:
            print "Received unknown message : %s" % line
            self.transport.loseConnection()

    def connectionLost(self,reason):
       print "Conection closed with %s" % (self.transport.getPeer())
       reactor.stop()

    def speak_proto(self,message):
        if self.state=='INI' and message[0].strip() == 'READY TO ACCEPT REQUESTS':
            if arguments.verbose: print "[%s] Sending register request" % datetime.datetime.now()
            self.transport.write("REGISTER:\r\n")
            self.state='REG'
        elif self.state=='REG' and message[0].strip() =='REGISTERED':
            if arguments.verbose: print "[%s] Registered, sending job request" % datetime.datetime.now()
            self.factory.clientID=message[1].strip()
            self.transport.write("REQUEST JOB:%s\r\n" %self.factory.clientID)
            self.state='RJOB'
        elif self.state=='RJOB' and message[0].strip() =='JOB SEGMENT':
            if arguments.verbose: print "[%s] Receiving job segment" % datetime.datetime.now()
            #Take the first, and hopefully the only, element of the list returned by pickle
            self.factory.job_segment=pickle.loads(message[1].strip())[0]
            print "[%s] Assigned job: %s" % (datetime.datetime.now(),self.factory.job_segment)
            self.factory.factorize_with_limits(self.factory.job_segment.num,[],self.factory.job_segment.segment[0],self.factory.job_segment.segment[1])
            self.transport.loseConnection()





#Factor Client Factory
class FCFactory(protocol.ClientFactory):

    #Identitification for this client, assigned by the server
    clientID=None

    #Factoring job to solve
    job_segment=None

    def buildProtocol(self,addr):
        return FCProtocol(self)

    def clientConnectionFailed(self,connector,reason):
        Address=connector.getDestination()
        print "Could not connect to host %s port %d, due to %s" % (Address.host,Address.port,reason)
        reactor.stop()

    #Parameters: compnum.- An integer to factorize
    #           own_results.- list to store the factors found during the execution of the
    #             function.  Belongs to a multiprocessing Manager so it's visible outside the
    #             process
    #           candidate.- The first candidate to start looking for factors
    #           last_candidate.- The last candidate to try
    #Return:  The list of factors found, with duplacates
    def factorize_with_limits(self,compnum,own_results,candidate=2,last_candidate=2):
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
                compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += 1 #Now candidate equals 3
        if candidate == 3: #This condition is here because the initial value of candidate may be different from 2
            while compnum%candidate == 0:
                compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += 2 #Now candidate equals 5
        if candidate == 4: candidate = 5 #Upgrade to the next meaninful candidate
        if candidate == 5: #This condition is here because the initial value of candidate may be different from 2
            while compnum%candidate == 0:
                compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += 2 #Now candidate equals 7
    #----MAIN LOOP----
        while candidate <= max_candidate:
            while compnum%candidate == 0:
                compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += increment[0] #This increment depends on the incremnet list selected bejore
            while compnum%candidate == 0:
                compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += increment[1] #This increment depends on the incremnet list selected bejore
            while compnum%candidate == 0:
                compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += increment[2] #This increment depends on the incremnet list selected bejore
            while compnum%candidate == 0:
                compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate)
            candidate += increment[3] #This increment depends on the incremnet list selected bejore
        if compnum != 1: own_results.append(compnum)
        print "[%s] factors of %d: %s" % (datetime.datetime.now(), compnum,own_results)

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




#Parameters: none
#Return value: the arguments found in the command line
def parse_arguments():
    '''Parses the command line arguments'''
    parser=argparse.ArgumentParser(description="Find the prime factors of an integer numberi within a segments, all supplied by a server")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("host",default='localhost', help="Host name or IP to connect to")
    parser.add_argument("port", help="Server port to connect to", type=int)
    return parser.parse_args()


def main():
    reactor.connectTCP(arguments.host,arguments.port,FCFactory())
    reactor.run()

if __name__ == '__main__':
    arguments=parse_arguments()
    main()

