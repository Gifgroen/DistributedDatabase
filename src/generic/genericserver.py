from os import sep
import sys

from twisted.python import log
from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory, Protocol

from serverstatemachine import BinaryDataReceiverProtocol

class ProtoMessageServer(object):
    
    @staticmethod
    def addServerOptions(parser):
        parser.add_option("-c", "--cert", dest="certificateFile", default="sslcert/cert.pem", help="load certificate from FILE (PEM format)", metavar="FILE")
        parser.add_option("-k", "--key", dest="privateKeyFile", default="sslcert/key.pem", help="load private key from FILE (PEM format)", metavar="FILE")
        parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
        parser.add_option("-p", "--port", type="int", dest="port", default=8989, help="set server PORT", metavar="PORT")
    
    def __init__(self, options, args):
        self.port = options.port
        self.sslCertificateFile = options.certificateFile
        self.sslPrivateKeyFile = options.privateKeyFile
        self.enableLogging = options.verbose
        
    def setHeaderParserClass(self, headerParserClass):
        self.headerParserClass = headerParserClass
        
    def _genFactory(self):
        factory = Factory()
        factory.connections = []
        factory.server = self
        factory.protocol = BinaryDataReceiverProtocol
        factory.headerParserClass = self.headerParserClass
        return factory
        
    def run(self):
        if self.enableLogging:
            log.startLogging(sys.stdout)
        
        reactor.listenSSL(self.port, self._genFactory(),
                          ssl.DefaultOpenSSLContextFactory(
                            self.sslPrivateKeyFile, self.sslCertificateFile))
        reactor.run()