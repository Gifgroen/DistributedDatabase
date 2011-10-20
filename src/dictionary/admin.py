from generic.communication_pb2 import StorageAdminResponse, StorageAdminRequestContainer, StorageAdminRecoveryOperation, StorageAdminServerLocation

from generic.genericserver import FixedLengthMessageServer
from generic.protocol import BinaryMessageProtocol
from storageclient import SimpleStorageTestClient
from twisted.python import log


class DictionaryAdminRequestHandler(object):
    def __init__(self, protocol):
        self.protocol = protocol
    
    
    def parsedMessage(self, msgData):
        """
         handle admin requests
         -> add new replica slave
        """
        log.msg("admin message received")
        pass
    
class DictionaryAdminServer(FixedLengthMessageServer):
    def __init__(self, options, args, server):
        super(DictionaryAdminServer, self).__init__(options, args, options.admin_port)
        self.factory.handlerClass = DictionaryAdminRequestHandler
        self.factory.protocol = BinaryMessageProtocol
        self.factory.protocolVersion = 0b1
        self.factory.dictionaryServer = server
        
        
        
