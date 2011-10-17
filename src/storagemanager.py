from storageclient import SimpleStorageTestClient
from generic.protobufconnection import BlockingProtoBufConnection
from threading import Thread
from time import time, sleep
import socket

from generic.communication_pb2 import StorageAdminResponse, StorageAdminRequestContainer, StorageAdminRecoveryOperation, StorageAdminServerLocation

HEARTBEAT_SECONDS = 30

STAND_BY_LIST = [] # Connections
ACTIVE_LIST = [] # Raidgroups


class AdminStorageClient(object):
    def __init__(self, host, port):
        self.connection = BlockingProtoBufConnection(StorageAdminResponse)
        self.connection.start(host, port)
        
    def _send(self, msg, opp):
        container = StorageAdminRequestContainer()
        container.operation = opp
        container.messageData = msg.SerializeToString()
        self.connection.sendMsg(container)
        
    def _checkResponse(self):
        response = self.connection.readMsg()
        if response.status == StorageAdminResponse.OK:
            return True
        print response.errorMsg
        return False
        
    def setXORServer(self, host, port):
        serverMsg = StorageAdminServerLocation()
        serverMsg.host = host
        serverMsg.port = port
        self._send(serverMsg, StorageAdminRequestContainer.SET_XOR_SERVER)
        return self._checkResponse()
    
    def recoverDataFrom(self, hostA, portA, hostB, portB):
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
        except socket.error:
            return False
        return True
        
    def setXORServer(self, connection):
        self.adminClient.setXORServer(connection.host, connection.clientPort)
        
    def recoverDataFrom(self, server1, server2):
        self.adminClient.recoverDataFrom(
            server1.host, server1.clientPort,
            server2.host, server2.clientPort
        )
        
    def __repr__(self):
        return '%s:[%d|%d]' % (self.host, self.clientPort, self.adminPort)


class RaidGroup(object):
    
    def __init__(self, a, b, x):
        self.serverA = a
        self.serverB = b
        self.xorServer = x
        print 'set serverA xor'
        self.serverA.setXORServer(x)
        print 'set serverB xor'
        self.serverB.setXORServer(x)
        print 'servers started'
        
    def _recover(self, server1, server2):
        newServer = STAND_BY_LIST.pop()
        newServer.recoverDataFrom(server1, server2)
        return newServer
        
    def _recoverServer(self, runningServer, xor):
        newServer = self._recover(runningServer, xor)
        newServer.setXORServer(self.xorServer)
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
        
        if self.xorServer is not None and not self.xorServer.sendHeartbeat():
            print 'Recover XOR server'
            self.xorServer = self._recoverXORServer()
            
    def __repr__(self):
        return '(A=%s,B=%s,X=%s)' % (self.serverA, self.serverB, self.xorServer)
            
def heartBeatJob():
    while True:
        print 'heartBeatJob'
        start = time()
        for group in ACTIVE_LIST:
            group.check()
        # check again in heartbeat time seconds (minus the time the job took)
        sleep_secs = max(HEARTBEAT_SECONDS - (int(time() - start)), 0)
        print 'sleep %d seconds' % sleep_secs
        sleep(sleep_secs)
            
    
def startup():
    t = Thread(target=heartBeatJob, name='HeartBeatJob')
    t.start()
    
def addServer(host, clientPort, adminPort):
    newServer = Connection(host, clientPort, adminPort)
    STAND_BY_LIST.append(newServer)
    

def _createGroup(testing):
    servers = []
    for standby in STAND_BY_LIST:
        if standby.host not in [server.host for server in servers] or testing:
            servers.append(standby)
            if len(servers) == 3:
                return servers

def startNewGroup(testing=False):
    servers = _createGroup(testing)
    print servers
    if servers:
        for server in servers:
            STAND_BY_LIST.remove(server)
        newGroup = RaidGroup(*servers)
        ACTIVE_LIST.append(newGroup)
        return True
    return False
    
def testSetup():
    startup()
    addServer('localhost', 8080, 8081)
    addServer('localhost', 8082, 8083)
    addServer('localhost', 8084, 8085)
    print 'STAND_BY_LIST', STAND_BY_LIST
    startNewGroup(True)
    print 'ACTIVE_LIST', ACTIVE_LIST
