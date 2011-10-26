from generic.communication_pb2 import RequestContainer, DictionaryLocation, AdminResponse, DictionaryKeys

from generic.genericserver import FixedLengthMessageServer
from generic.protocol import BinaryMessageProtocol
from storageclient import SimpleStorageTestClient
from twisted.python import log


class DictionaryAdminRequestHandler(object):
    def __init__(self, protocol):
        self.protocol = protocol
        self.dictServer = self.protocol.factory.dictionaryServer

    def setSlave(self, host, port):
        replica = {"host": host, "port": port}
        if replica not in self.dictServer.factory.replicaList:
            self.dictServer.factory.replicaList.append(replica)
            self._reply()
        else: 
            self._reply("Replica already exists")
            
    def setMaster(self, host, port):
        self.dictServer.factory.master = {"host": host, "port": port}
        self._reply()

    def _reply(self, error=None):
        reply = AdminResponse()
        if error:
            reply.status = AdminResponse.ERROR
            reply.errorMsg = error
        else:
            reply.status = AdminResponse.OK
        self.protocol.writeMsg(reply)

    def parsedMessage(self, msgData):
        log.msg(">>> admin message received")
        incoming = RequestContainer()
        incoming.ParseFromString(msgData)
        if incoming.notification == RequestContainer.NEW_SLAVE:
            # notify self.protocol.dictServer of new replica slave
            msg = DictionaryLocation()
            msg.ParseFromString(incoming.messageData)
            self.setSlave(msg.host, msg.port)
            log.msg("New slave set: ", msg.host, " at ", msg.port)
        elif incoming.notification == RequestContainer.NEW_MASTER:
            msg = DictionaryLocation()
            msg.ParseFromString(incoming.messageData)
            self.setMaster(msg.host, msg.port)
            log.msg("New master set: ", msg.host, " at ", msg.port)
        elif incoming.notification == RequestContainer.IS_MASTER:
            print("I AM THE NEW MASTER :D")
            self._reply()
        elif incoming.notification == RequestContainer.IS_SLAVE:
            print("I am a humble slave")
            self._reply()
        else:
            self._reply("Unknown dictionary admin operation")
            raise Exception("Unkown dictionary admin operation")
    
class DictionaryAdminServer(FixedLengthMessageServer):
    def __init__(self, options, args, server):
        super(DictionaryAdminServer, self).__init__(options, args, options.admin_port)
        self.factory.handlerClass = DictionaryAdminRequestHandler
        self.factory.protocol = BinaryMessageProtocol
        self.factory.protocolVersion = 0b1

        # the dictServer it manages
        self.factory.dictionaryServer = server
        
        
        
