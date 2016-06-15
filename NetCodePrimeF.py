#!/usr/bin/env python

from twisted.internet import reactor
from twisted.internet.protocol import Protocol,Factory
from twisted.internet.task import LoopingCall
from twisted.protocols import basic
import datetime
import md5
from multiprocessing import Queue
import NetJob

external_port=8000
internal_port=8010

#Remote prime factor helper network code
#Protocol class
class PFServerProtocol(basic.LineReceiver): 

    messages={'REGISTER': 'register',
              'REQUEST JOB': 'serve_request',
              'SEND RESULTS': 'receive_results'}

    peer=None #Address object

    def connectionLost(self,reason):
       print "Conection closed with %s due to %s" % (self.transport.getPeer(),reason)

    def connectionMade(self):
        self.peer=self.transport.getPeer()
        print "Connection received from host %s port %d" % (self.peer.host,self.peer.port)
        self.sendLine("READY TO ACCEPT REQUESTS:")

    def lineReceived(self,line):
        print "line received:\n%s" %line
        proto_msg=line.split(':',1)
        if len(proto_msg) == 2:
            next_step_proto=self.messages.get(proto_msg[0].strip(),'unknown_message')
            getattr(self,next_step_proto)(proto_msg[1].strip())
        else:
            self.unknown_message(line)
            self.transport.loseConnection()

    def unknown_message(self,message):
        self.transport.write("UNKNOWN REQUEST: %s\r\n" % message)
        self.transport.loseConnection()

    def register(self,message):
        reg_time=datetime.datetime.now()
        reg_md5=md5.new(str(self.peer.host) + str(reg_time)).hexdigest()
        print "Register client from : %s at %s with md5 %s" % (self.peer.host,reg_time,reg_md5)
        if self.factory.reg_client(self.peer.host,reg_md5,reg_time):
            self.transport.write("REGISTERED:%s\r\n" % reg_md5)
            print "Client registered"

    def serve_request(self,job_ID):
        '''Run when the "REQUEST JOB" protocol command is received from the client'''
        print "Host %s requesting factoring job" % self.peer.host
        if job_ID in self.factory.registered_clients: #Place job request in queue
            NetJob.NetJob(job_ID)
            self.factory.reqres_queue.put(,'REQUEST'))
            print "Request sent to parent, waiting for response"
            #@ Call a function in the factory that possibly returns a deferred and waits
            # for the factor job to arrive @#
        else:
            print "Client not registered"
            self.transport.loseConnection()

    def receive_results(self):
        pass




#Factory class
class PFServerProtocolFactory(Factory): 
    protocol=PFServerProtocol

    #Client IP; client ID; registration time
    registered_clients=dict()

    def __init__(self,reqres_queue,job_queue):
        self.reqres_queue=reqres_queue
        self.job_queue=job_queue

    def reg_client(self,host,MD5,timestamp):
        '''Keeps a record of registered clients'''
        if not MD5 in self.registered_clients:
            self.registered_clients[MD5]={'HOST': host, 'REG_TIME': timestamp}
            return True

    def get_assigned_job(self,):


#Inter process comunications
class IPCProtocol(basic.LineReceiver):

    def lineReceived(self,line):
        self.transport.loseConnection()
        reactor.stop()

class IPCFactory(Factory):

    protocol=IPCProtocol

    def __init__(self):
        pass

def server_netcode(reqres_queue,job_queue):

    print "Starting server in port %d" % external_port
    reactor.listenTCP(external_port,PFServerProtocolFactory(reqres_queue,job_queue))
    print "Starting server in port %d and interface localhost" % internal_port
    reactor.listenTCP(internal_port,IPCFactory(),interface='localhost')
    reactor.run()

if __name__ == "__main__":
    server_netcode(Queue(),Queue())

