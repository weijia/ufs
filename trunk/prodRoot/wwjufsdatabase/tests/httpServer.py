from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

### Protocol Implementation

received = ""
# This is just about the simplest possible protocol
class Echo(Protocol):
    def dataReceived(self, data):
        """As soon as any data is received, write it back."""
        #self.transport.write(data)
        global received
        received += data
        if len(received.split('\n')) > 3:
            f = open("d:/dump.obj","rb")
            self.transport.write(f.read())
            f.close()
            self.transport.loseConnection()


def main():
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(8805, f)
    reactor.run()

if __name__ == '__main__':
    main()