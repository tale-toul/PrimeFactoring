#! /usr/bin/env python

import argparse
from twisted.internet import reactor,protocol
from twisted.protocols import basic

#Factor Client Protocol
class FCProtocol(basic.LineReceiver):

     def connectionMade(self):
        if arguments.verbose: print ("Connection made")

     def lineReceived(self,line):
        proto_msg=line.split(':',1)
        if len(proto_msg) == 2 and proto_msg[0] == 'READY TO ACCEPT REQUESTS':
            print "Sending register request"
            self.transport.write("REGISTER:\r\n")
        else:
            print "Protocol message unknown"
            self.transport.loseConnection()



#Factor Client Factory
class FCFactory(protocol.ClientFactory):
    protocol=FCProtocol

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

