#!/usr/bin/env python

from twisted.internet import reactor
from twisted.internet.protocol import Protocol,Factory
from twisted.protocols import basic

external_port=8000
internal_port=8010

#Remote prime factor helper network code
#Protocol class
class PFServerProtocol(basic.LineReceiver): 

    def connectionLost(self,reason):
       print "Conection closed with %s due to %s" % (self.transport.getPeer(),reason)

    def connectionMade(self):
        peer=self.transport.getPeer()
        print "Connection received from host %s port %d" % (peer.host,peer.port)
        self.sendLine("READY TO ACCEPT REQUESTS:")

    def lineReceived(self,line):
        print "line received:\n%s" %line
        proto_msg=line.split(':',1)
        if len(proto_msg) == 2:
            next_step_proto=self.factory.messages.get(proto_msg[0],'UNKNOWN MESSAGE')




#Factory class
class PFServerProtocolFactory(Factory): 
    protocol=PFServerProtocol

    messages={'REGISTER': 1}



#Inter process comunications
class IPCProtocol(basic.LineReceiver):

    def lineReceived(self,line):
        self.transport.loseConnection()
        reactor.stop()

class IPCFactory(Factory):
    protocol=IPCProtocol

def server_netcode():

    print "Starting server in port %d" % external_port
    reactor.listenTCP(external_port,PFServerProtocolFactory())
    print "Starting server in port %d and interface localhost" % internal_port
    reactor.listenTCP(internal_port,IPCFactory(),interface='localhost')
    reactor.run()

if __name__ == "__main__":
    server_netcode()

