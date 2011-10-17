from generic.communication_pb2 import StorageAdminResponse, StorageAdminRequestContainer, StorageAdminRecoveryOperation, StorageAdminServerLocation

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
            msg.ParseFromString(incoming.messageData)
            self._handleRecovery(msg)
        elif incoming.operation == StorageAdminRequestContainer.SET_XOR_SERVER:
            msg = StorageAdminServerLocation()
            msg.ParseFromString(incoming.messageData)
            self._handleSetXORServer(msg)
        else:
            raise Exception("Unkown storage admin operation")
    
    def _reply(self, error=None):
        reply = StorageAdminResponse()
        if error:
            reply.status = StorageAdminResponse.ERROR
            reply.errorMsg = error
        else:
            reply.status = StorageAdminResponse.OK
        self.protocol.writeMsg(reply)
        
    def _handleSetXORServer(self, serverMsg):
        log.msg("Handle set XOR server")
        storageServer = self.protocol.factory.storageServer
        if storageServer.factory.xor_server_connection is not None:
            storageServer.factory.xor_server_connection.stop()
        log.msg('create xor partner connection')
        storageServer.factory.xor_server_connection = XORPartnerConnection(serverMsg.host, serverMsg.port)
        log.msg('.start()')
        storageServer.factory.xor_server_connection.start()
        log.msg('relpy')
        self._reply()
        log.msg('reply finished')
    
    def _recover(self, connA, connB):        
        CHUNK_SIZE = 1024 #1kb
        # TODO
        self._reply()
    
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
        
    