from twisted.internet import reactor
from twisted.internet.protocol import Protocol,Factory


class PFServerProtocol(Protocol): 
    pass

class PFServerProtocolFactory(Factory): 
    protocol=PFServerProtocol


def server_netcode():
    port=8000

    reactor.listenTCP(port,PFServerProtocolFactory())
    reactor.run()

if __name__ == "__main__":
    server_netcode()

