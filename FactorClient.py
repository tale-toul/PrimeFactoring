#! /usr/bin/env python

import argparse
from twisted.internet import reactor,protocol
from twisted.protocols import basic

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
       print "Conection closed with %s due to %s" % (self.transport.getPeer(),reason)
       reactor.stop()

    def speak_proto(self,message):
        if self.state=='INI' and message[0].strip() == 'READY TO ACCEPT REQUESTS':
            if arguments.verbose: print "Sending register request"
            self.transport.write("REGISTER:\r\n")
            self.state='REG'
        elif self.state=='REG' and message[0].strip() =='REGISTERED':
            if arguments.verbose: print "Sending job request"
            self.factory.ID=message[1].strip()
            self.transport.write("REQUEST JOB:%s\r\n" %self.factory.ID)
            self.state='RJOB'
        #elif: self.state=='RJOB' and message[0] =='




#Factor Client Factory
class FCFactory(protocol.ClientFactory):

    ID=None

    def buildProtocol(self,addr):
        return FCProtocol(self)

    def clientConnectionFailed(self,connector,reason):
        Address=connector.getDestination()
        print "Could not connect to host %s port %d, due to %s" % (Address.host,Address.port,reason)
        reactor.stop()



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

