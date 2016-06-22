#!/usr/bin/env python

from twisted.internet import reactor,defer
from twisted.internet.protocol import Protocol,Factory
from twisted.internet.task import LoopingCall
from twisted.protocols import basic
import datetime
import md5
from multiprocessing import Queue
import pickle
import NetJob

external_port=8000
internal_port=8010

#Remote prime factor helper network code
#Protocol class
class PFServerProtocol(basic.LineReceiver): 

    #Messages accepted by this network server
    messages={'REGISTER': 'register',
              'REQUEST JOB': 'serve_request',
              'SEND RESULTS': 'receive_results',
              'STOP REACTOR': 'stop_reactor'}

    peer=None #Address object
    loops=5 #Maximun number of attempts to get the jobs from the parent, once the request
            # has been sent
    job_retreived=None #Job retreived from the jobs queue
    lpc_fetch_jobs=None #Looping Call to look for jobs in the job queue

    def connectionLost(self,reason):
        print "Conection closed with %s with message: %s" % (self.transport.getPeer().host,reason.getErrorMessage())

    def connectionMade(self):
        self.peer=self.transport.getPeer()
        print "Connection received from host %s port %d" % (self.peer.host,self.peer.port)
        self.sendLine("READY TO ACCEPT REQUESTS:")

    def lineReceived(self,line):
        proto_msg=line.split(':',1)
        if len(proto_msg) == 2:
            next_step_proto=self.messages.get(proto_msg[0].strip(),'unknown_message')
            getattr(self,next_step_proto)(proto_msg[1].strip())
        else:
            print "Unkknow message %s" % line
            self.unknown_message(line)
            self.transport.loseConnection()

    def unknown_message(self,message):
        self.transport.write("UNKNOWN REQUEST: %s\r\n" % message)
        self.transport.loseConnection()

    def register(self,message):
        reg_time=datetime.datetime.now()
        reg_md5=md5.new(str(self.peer.host) + str(reg_time)).hexdigest()
        print "Registering client from: %s at %s with MD5: %s" % (self.peer.host,reg_time,reg_md5)
        if self.factory.reg_client(self.peer.host,reg_md5,reg_time):
            self.transport.write("REGISTERED:%s\r\n" % reg_md5)
            print "Client registered"

    #Parameters: clientID.- The md5 id assigned to the client when it previously
    #                   registered. The protocol expects this ID to be the only component
    #                   of the message after the colom
    def serve_request(self,clientID):
        '''Run when the "REQUEST JOB" protocol command is received from the client'''
        print "Host %s (%s) requesting job" % (self.peer.host,clientID)
        if clientID in self.factory.registered_clients: #Place job request in queue
            request=NetJob.NetJob(clientID,'REQUEST')
            self.factory.request_queue.put(request)
            print "Request sent to parent, waiting for response"
            self.wait_for_job(clientID)
        else:
            print "Client not registered"
            self.transport.loseConnection()

    def wait_for_job(self,clientID):
        '''Start the looping call to the function that collects the jobs delivered by the
        parent process.  Starts and tries to get the job for the current net client'''
        if not self.factory.lpc_order_jobs.running: #Start the loop that orders the jobs found in the queue
            self.factory.lpc_order_jobs.start(3) #This is run from the factory
        self.lpc_fetch_jobs=LoopingCall(self.fetch_job,clientID)
        fetch_deferred=self.lpc_fetch_jobs.start(3.5) #This is run in the protocol
        fetch_deferred.addCallbacks(self.job_found,self.job_not_found)

    def fetch_job(self,clientID):
        if self.loops: #Run for a maximun number of loops 
            self.loops -=1
            self.job_retreived=self.factory.ordered_jobs.pop(clientID,None)
            if self.job_retreived:
                self.lpc_fetch_jobs.stop()
        else:#If we didn't find a suitable job within time, call Errback
            self.loops=5 #@I don't like using this constant here@#
            raise Exception('Could not get job from parent, timeout')

    def job_found(self,result):
        print "Job received from parent, sending to client: %s" % self.job_retreived
        pickled_job=pickle.dumps(self.job_retreived,pickle.HIGHEST_PROTOCOL )
        self.transport.write("JOB SEGMENT:%s\r\n" % pickled_job)

    def job_not_found(self,failure):
        fmsg=failure.getErrorMessage()
        print fmsg
        self.transport.write("REQUEST TIMEOUT:fmsg\r\n")
        self.transport.loseConnection()

    def receive_results(self,pickle_job):
        '''Receive the results from a client.  The client must be already registered and
            the job must have been previously assigned '''
        self.job_result=pickle.loads(pickle_job) #Get the NetJob back from pickle form
        if self.job_result.worker_ID in self.factory.registered_clients: #Place job request in queue
#@I should also check that the result correponds with a previous request@#
            self.factory.result_queue.put(self.job_result)
            print "Results sent to parent, waiting for ACK"
            self.wait_for_job(self.job_result.worker_ID)


#ONLY ACCEPTED WHEN COMMING FROM LOCALHOST
    def stop_reactor(self,message):
        '''Stop the reactor when asked by the parent, or any other local process for that
        matter'''
        if self.transport.getPeer().host == '127.0.0.1':
            reactor.stop()
        else:
            print self.transport.getPeer()


#Factory class
class PFServerProtocolFactory(Factory): 
    protocol=PFServerProtocol


    #Client IP; client ID; registration time
    registered_clients=dict()

    #Dictionary of jobs returned by the parent process
    ordered_jobs=dict()

    def __init__(self,request_queue,result_queue,job_queue):
        self.request_queue=request_queue
        self.result_queue=result_queue
        self.job_queue=job_queue
        #Looping call to order jobs from the job queue 
        self.lpc_order_jobs=LoopingCall(self.order_job)

    def reg_client(self,host,MD5,timestamp):
        '''Keeps a record of registered clients'''
        if not MD5 in self.registered_clients:
            self.registered_clients[MD5]={'HOST': host, 'REG_TIME': timestamp}
            return True

    def order_job(self):
        '''Get the elements in the jobs queue and add them to a dictionary indexed by
        clientID.  A client may have more than one job assigned to it, so the content of
        the dictionary is a list of NetJob objects '''
        while not self.job_queue.empty():
            response=self.job_queue.get()
            if response.worker_ID in self.ordered_jobs:
                self.ordered_jobs[response.worker_ID].append(response)
            else:
                self.ordered_jobs[response.worker_ID]=[response]



#Parameters: request_queue.- Multiprocessing Queue used by this module to place NetJob
#               objects representing job requests for the parent process. It's shared with
#               the parent process.
#            result_queue.- Multiprocessing Queue used by this module to place the NetJob
#            objects representing job results for the parent process.  It's share with the
#            parent process
#            job_queue.- Multiprocessing Queue used by the parent process to place the
#            jobs assigned to network clients. This process reads from it and delivers the
#            jobs to the clients
def server_netcode(request_queue,result_queue,job_queue):
    '''this is the main function in this package, starts the twisted reactor, opens the
    sockets to listen to incoming connections, serves requests, etc.'''
    factory=PFServerProtocolFactory(request_queue,result_queue,job_queue)
    print "[%s] Starting server in port %d" % (datetime.datetime.now(),external_port)
    reactor.listenTCP(external_port,factory)
    print "[%s] Starting server in port %d and interface localhost" % (datetime.datetime.now(),internal_port)
    reactor.listenTCP(internal_port,factory,interface='localhost')
    reactor.run()

if __name__ == "__main__":
    server_netcode(Queue(),Queue(),Queue())

