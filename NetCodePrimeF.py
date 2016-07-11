#!/usr/bin/env python

from twisted.internet import reactor,defer
from twisted.internet.protocol import Protocol,Factory
from twisted.internet.task import LoopingCall
from twisted.protocols import basic
import datetime
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
              'STOP REACTOR': 'stop_reactor',
              'CLIENT TIMEOUT': 'client_timeout'}

    peer=None #Address object
    job_retreived=None #Job retreived from the jobs queue
    lpc_fetch_jobs=None #Looping Call to look for jobs in the job queue
    stop_fetch_job=None #Time out flag to be set by the client

    def connectionLost(self,reason):
        stop_fetch_job=True
        # When a connection with a client is closed, also stop looking for jobs or ACKs
        # for that client, if we are doing so, that's it
        if self.lpc_fetch_jobs and self.lpc_fetch_jobs.running:
            self.lpc_fetch_jobs.stop()
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

    def register(self,clientID):
        '''Registers a client'''
        print "Registering client from: %s:%s with MD5: %s" % (self.peer.host,self.peer.port,clientID[:7])
        if self.factory.reg_client(self.peer.host,clientID):
            self.transport.write("REGISTERED:\r\n")
            print "Client registered"
        else:
            print "Client cannot be registered. Already registered?"
#@Send a protocol message back to the client@#
            self.transport.loseConnection()

    #Parameters: pickled_request.- The NetJob object sent by the client
    def serve_request(self,pickled_request):
        '''Receives a request from the client and passes it to the parent process to be
        served. Run when the "REQUEST JOB" protocol command is received from the client'''
        job_request=pickle.loads(pickled_request) #Get the NetJob back from pickle form
        request_ID=job_request.job_ID #Store the request_ID during this connection
        print "Host %s (%s) requesting job %s" % (self.peer.host,job_request.worker_ID[:7],request_ID[:7])
        if job_request.worker_ID in self.factory.registered_clients: #If client registered, place job request in queue
            if job_request.job_ID in self.factory.registered_clients[job_request.worker_ID]:
                print "Job request %s already received, ignoring" % job_request.job_ID
            else:
                self.factory.registered_clients[job_request.worker_ID][job_request.job_ID]=None
                self.factory.request_queue.put(job_request)
                print "Request sent to parent, waiting for response"
                self.wait_for_job(job_request.worker_ID,request_ID,None)
        else:
            print "Client not registered"
            self.transport.loseConnection()

    def client_timeout(self,netjob):
        '''This function is called when the client send a timeout message, it doesn't do
        much, just prints a message, the actual action is done in the connectionLost
        function where the looping call is stopped '''
        job_tmo=pickle.loads(netjob) #Get the NetJob back from pickle form
        if job_tmo.worker_ID in self.factory.registered_clients:
            if job_tmo.job_ID in self.factory.registered_clients[job_tmo.worker_ID]:
                self.factory.registered_clients[job_tmo.worker_ID].pop(job_tmo.job_ID)
                print "Job %s cancelled" % job_tmo.job_ID
                self.stop_fetch_job=True
            else:
                print "Timeout for non existing job %s" % job_tmo.job_ID
        else:
            print "Client not registered"
            self.transport.loseConnection()

    def wait_for_job(self,clientID,request_ID,job_response):
        '''Start the looping call to the function that collects the jobs delivered by the
        parent process.  Starts and tries to get the job for the current net client'''
        if not self.factory.lpc_order_jobs.running: #Start the loop that orders the jobs found in the queue
            self.factory.lpc_order_jobs.start(3) #This is run from the factory
        self.lpc_fetch_jobs=LoopingCall(self.fetch_job,clientID,request_ID)
        fetch_deferred=self.lpc_fetch_jobs.start(3.5) #This is run in the protocol
        fetch_deferred.addCallback(self.job_found)
        fetch_deferred.addErrback(self.job_not_found,job_response)

    def fetch_job(self,clientID,request_ID):
        if self.stop_fetch_job: raise Exception('Time out fetching job %s' % request_ID)
        if clientID in self.factory.registered_clients:
            self.job_retreived=self.factory.registered_clients[clientID].get(request_ID,None)
            if self.job_retreived:
                if self.job_retreived.is_ack(): #if it's an ACK remove the job from registered_clients
                    self.factory.registered_clients[clientID].pop(request_ID)
                self.lpc_fetch_jobs.stop()
        else: #Client not registered!!!
            raise Exception('Client %s not registered' % clientID)

    def job_found(self,result):
        if not self.stop_fetch_job:
            if self.job_retreived.is_ack():
                print "Ack received from parent, sendign to client: %s" % self.job_retreived
            elif self.job_retreived.is_response():
                print "Job received from parent, sending to client: %s" % self.job_retreived
            pickled_job=pickle.dumps(self.job_retreived,pickle.HIGHEST_PROTOCOL )
            self.transport.write("JOB SEGMENT:%s\r\n" % pickled_job)

    def job_not_found(self,failure,job_response):
        fmsg=failure.getErrorMessage()
        print "[NCd] %s" % fmsg
        if job_response: #Put the job response back in
            self.factory.registered_clients[job_response.worker_ID][job_response.job_ID]=job_response
        self.transport.write("REQUEST TIMEOUT:%s\r\n" % fmsg)

    def receive_results(self,pickle_job):
        '''Receive the results from a client.  The client must be already registered and
            the job must have been previously assigned '''
        job_results=pickle.loads(pickle_job) #Get the NetJob back from pickle form
        request_ID=job_results.job_ID #Store the request_ID during this connection
        if job_results.is_result():
            if job_results.worker_ID in self.factory.registered_clients: #client registered?
                #Does the job_ID exist and is a response from a request?
                if request_ID in self.factory.registered_clients[job_results.worker_ID] and self.factory.registered_clients[job_results.worker_ID][request_ID].is_response():
                    self.factory.result_queue.put(job_results)
                    #Remove the job from registered clients so it doesn't mess up the waiting for ack process
                    job_response=self.factory.registered_clients[job_results.worker_ID].get(request_ID) 
                    self.factory.registered_clients[job_results.worker_ID][request_ID]=None
                    print "Results sent to parent, waiting for ACK"
                    self.wait_for_job(job_results.worker_ID,request_ID,job_response) #Wait for ACK from parent
                else:
                    print "Results received when not expected, closeing down connection"
                    self.transport.loseConnection()
            else:
                print "Client not registered, closeing down connection"
                self.transport.loseConnection()
        else:
            print "This is not a result object, closing down connection"
#@Send a protocol message to the client to warn him of the situation
            self.transport.loseConnection()


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


    #This data structure is a dictionary of dictionaries:
    #   -The outer dictionary has keys (clientID) and value the inner dictionary.
    #   -The inner dictionary has keys: 'host' with value <IP address of the client>
    #                                   zero or more 'job_ID' with value a NetJob object
    registered_clients=dict()

    def __init__(self,request_queue,result_queue,job_queue):
        self.request_queue=request_queue
        self.result_queue=result_queue
        self.job_queue=job_queue
        #Looping call to order jobs from the job queue 
        self.lpc_order_jobs=LoopingCall(self.order_job)

    def reg_client(self,host,clientID):
        '''Keeps a record of registered clients'''
        if not clientID in self.registered_clients:
            self.registered_clients[clientID]={ 'host': host}
            return True

    def order_job(self):
        '''Get the elements in the jobs queue, where the parent put them and add them to a
        dictionary indexed by clientID.  A client may have several job assingments'''
        while not self.job_queue.empty():
            response=self.job_queue.get() #Get a NetJob object from the queue
            if response.worker_ID in self.registered_clients:
                #Every job back from the parent must have a previous request in registered_clients
                #@I'm not checking here if the response corresponds with an request; and the ack corresponds with a results @#
                if response.job_ID in self.registered_clients[response.worker_ID]:
                    self.registered_clients[response.worker_ID][response.job_ID]=response
                else:
                    print "Job %s not requested by client %s, discarding" % (response.job_ID[:7],response.worker_ID[:7])
            else:
                print "Job for a non-registered client:%s, discarding" % response.worker_ID[:7]



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

