from storageclient import SimpleStorageTestClient
from generic.protobufconnection import BlockingProtoBufConnection
from threading import Thread
from time import time, sleep

from generic.communication_pb2 import StorageAdminResponse, StorageAdminRequestContainer, StorageAdminRecoveryOperation, StorageAdminServer

HEARTBEAT_SECONDS = 30

STAND_BY_LIST = [] # Connections
ACTIVE_LIST = [] # Raidgroups


class AdminStorageClient(object):
    def __init__(self, host, port):
        self.connection = BlockingProtoBufConnection(StorageAdminResponse)
        self.connection.start(host, port)
        
    def _send(self, opp, msg):
        container = StorageAdminRequestContainer()
        container.operation = opp
        container.msgData = serverMessage.SerializeToString()
        self.connection.sendMsg(container)
        
    def _checkResponse(self):
        response = self.connection.readMsg()
        if response.status == StorageAdminResponse.OK:
            return True
        print response.errorMsg
        return False
        
    def setXORServer(host, port):
        serverMsg = StorageAdminServer()
        serverMsg.host = host
        serverMsg.port = port
        self._send(serverMsg, StorageAdminRequestContainer.SET_XOR_SERVER)
        return self._checkResponse()
    
    def recoverDataFrom(hostA, portA, hostB, portB):
        recoveryMsg = StorageAdminRecoveryOperation()
        recoveryMsg.serverA.host = hostA
        recoveryMsg.serverA.port = portA
        recoveryMsg.serverB.host = hostB
        recoveryMsg.serverB.port = portB
        self._send(serverMsg, StorageAdminRequestContainer.RECOVER_FROM)
        return self._checkResponse()

class Connection(object):
    
    def __init__(self, host, clientPort, adminPort):
        self.host = host
        self.clientPort = clientPort
        self.adminPort = adminPort
        self.client = SimpleStorageTestClient(host, clientPort)
        self.adminClient = AdminStorageClient(host, adminPort)
        
    def sendHeartbeat(self):
        try:
            self.client.readData(0, 1)
        except:
            return False
        return True
        
    def setXORServer(connection):
        self.adminClient.setXORServer(connection.host, connection.clientPort)
        
    def recoverDataFrom(server1, server2):
        self.adminClient.recoverDataFrom(
            server1.host, server1.clientPort,
            server2.host, server2.clientPort
        )


class RaidGroup(object):
    
    def __init__(self, a, b, x):
        self.serverA = a
        self.serverB = b
        self.xorServer = x
        
    def _recover(self, server1, server2):
        newServer = STAND_BY_LIST.pop()
        if not newServer: # this should be handled better of course... now everything stops.
            raise Exception("NEED NEW SERVER, BUT STAND_BY_LIST IS EMPTY")
        newServer.recoverDataFrom(server1, server2)
        return newServer
        
    def _recoverServer(self, runningServer, xor):
        newServer = self._recover(runningServer, xor)
        newServer.setXORserver(self.xorServer)
        return newServer
        
    def _recoverXORServer(self):
        newXORServer = self._recover(self.serverA, self.serverB)
        self.serverA.setXORserver(newXORServer)
        self.serverB.setXORserver(newXORServer)
        return newXORServer
        
    def check(self):
        if self.serverA is not None and not self.serverA.sendHeartbeat():
            print 'Recover server A'
            self.serverA = self._recoverServer(self.serverB, self.xorServer)
        
        if self.serverB is not None and not self.serverB.sendHeartbeat():
            print 'Recover server B'
            self.serverB = self._recoverServer(self.serverA, self.xorServer)
        
        if self.serverXOR is not None and not self.serverXOR.sendHeartbeat():
            print 'Recover XOR server'
            self.serverXOR = self._recoverXORServer()
            
            
def heartBeatJob():
    while True:
        start = time()
        for group in ACTIVE_LIST:
            group.check()
        # check again in heartbeat time seconds (minus the time the job took)
        sleep(max(int(time() - start - HEARTBEAT_SECONDS), 0))
            
    
def startup():
    t = Thread(target=heartBeatJob, name='HeartBeatJob')
    t.start()
    
def addServer(host, clientPort, adminPort):
    newServer = Connection(host, clientPort, adminPort)
    STAND_BY_LIST.append(newServer)
    

def _createGroup():
    servers = []
    for standby in STAND_BY_LIST:
        if standby.host not in [server.host for server in servers]:
            servers.append(standby)
            if len(servers) == 3:
                return servers

def startNewGroup():
    servers = _createGroup()
    if servers:
        newGroup = RaidGroup(*servers)
        ACTIVE_LIST.append(newGroup)
        return True
    return False

