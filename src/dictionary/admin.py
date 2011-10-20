#from generic.communication_pb2 import DictionaryAdmin

from generic.genericserver import FixedLengthMessageServer
from generic.protocol import BinaryMessageProtocol
from storageclient import SimpleStorageTestClient
from twisted.python import log


class DictionaryAdminRequestHandler(object):
    def __init__(self, protocol):
        self.protocol = protocol

    def setSlave(self, host, port):
        pass

    def parsedMessage(self, msgData):
        """
         handle admin requests
         -> notify self.protocol.dictServer of new replica slave
        """
        log.msg("admin message received")
        pass
    
class DictionaryAdminServer(FixedLengthMessageServer):
    def __init__(self, options, args, server):
        super(DictionaryAdminServer, self).__init__(options, args, options.admin_port)
        self.factory.handlerClass = DictionaryAdminRequestHandler
        self.factory.protocol = BinaryMessageProtocol
        self.factory.protocolVersion = 0b1

        # the dictServer it manages
        self.factory.dictionaryServer = server
        
        
        
