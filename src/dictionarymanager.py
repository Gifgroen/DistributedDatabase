# The server manager that initiates actions by sending messages to adminDictClients
from generic.communication_pb2 import AdminResponse, RequestContainer, DictionaryReplicaLocation, DictionaryKeys

from generic.protobufconnection import BlockingProtoBufConnection
from twisted.internet import reactor

# init new slave and notify dictServer

HEARTBEAT_SECONDS = 10 # low for testing

STAND_BY_LIST = [] # Connections
ACTIVE_LIST = [] # Raidgroups

class DictionaryAdminClient(object):
    """
    Host and port are the Admin client to which we want to connect
    """
    def __init__(self, host, port):
        self.connection = BlockingProtoBufConnection(AdminResponse)
        self.connection.start(host, port)
    
    """
    A message to send to a dictManager
    """
    def _send(self, msg, opp):
        internal = RequestContainer()
        internal.operation = opp
        if msg is not None:
            internal.messageData = msg.SerializeToString()
        self.connection.sendMsg(internal)
    
    
    """
    Check response
    """
    def _checkResponse(self):
        response = self.connection.readMsg()
        if response.status == AdminResponse.OK:
            return True
        print response.errorMsg
        return False
    
    """
    give the connected DictServer a new slave located at host:port
    """
    def setReplicaServer(self, host, port):
        serverMsg = DictionaryReplicaLocation()
        serverMsg.host = host
        serverMsg.port = port

        self._send(serverMsg, RequestContainer.NEW_SLAVE)
        return self._checkResponse()

    """
    Close the connection
    """
    def stop(self):
        print "Con closed"
        self.connection.stop()

if __name__ == "__main__":
    # the dictionary admin client to which we want to connect
    cli = DictionaryAdminClient("localhost", 8088)
    print cli.setReplicaServer("localhost", 8083)
    print cli.setReplicaServer("localhost", 8085)
    cli.stop()
    
