from generic.communication_pb2 import StorageAdminResponse, StorageAdminRequestContainer, StorageAdminRecoveryOperation, StorageAdminServer

from storage.xorpartnerconnection import XORPartnerConnection

from generic.genericserver import FixedLengthMessageServer
from generic.protocol import BinaryMessageProtocol
from storageclient import SimpleStorageTestClient
from twisted.python import log


class StorageAdminRequestHandler(object):
    def __init__(self, protocol):
        self.protocol = protocol
    
    
    def parsedMessage(self, msgData):
        incoming = StorageAdminRequestContainer()
        incoming.ParseFromString(msgData)
        if incoming.operation == StorageAdminRequestContainer.RECOVER_FROM:
            msg = StorageAdminRecoveryOperation()
            msg.parseFromString(incoming.msgData)
            self._handleRecovery(msg)
        elif incoming.operation == StorageAdminRequestContainer.SET_XOR_SERVER:
            msg = StorageAdminServer()
            msg.parseFromString(incoming.msgData)
            self._handleSetXorServer(msg)
        else:
            raise Exception("Unkown storage admin operation")
    
    
    def _handleSetXORServer(self, serverMsg):
        log.msg("Handle set XOR server")
        if self.factory.xor_server_connection is not None:
            self.factory.xor_server_connection.stop()
        self.factory.xor_server_connection = XORPartnerConnection(serverMsg.xhost, serverMsg.port)
        self.factory.xor_server_connection.start()
    
    def _recover(self, connA, connB):        
        CHUNK_SIZE = 1024 #1kb
        
    
    def _handleRecovery(self, recoveryMsg):
        log.msg("Handle recovery")
        connectionA = SimpleStorageTestClient(recoveryMsg.hostA, recoveryMsg.portA)
        connectionB = SimpleStorageTestClient(recoveryMsg.hostB, recoveryMsg.portB)
        self._recover(self, connectionA, connectionB)


class StorageAdminServer(FixedLengthMessageServer):
    def __init__(self, options, args, server):
        super(StorageAdminServer, self).__init__(options, args, options.admin_port)
        self.factory.handlerClass = StorageAdminRequestHandler
        self.factory.protocol = BinaryMessageProtocol
        self.factory.protocolVersion = 0b1
        self.factory.storageServer = server
        
    