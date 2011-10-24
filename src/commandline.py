"""
Import this module in a python terminal
"""

import sys, traceback
from time import sleep
from storageclient import SimpleStorageTestClient
from subprocess import Popen

LAST_PORT = 8080

storage_instances = {} #shortkey -> Popen
connections = {} #shortkey -->SimpleStorageTestClient


def terminateAll():
    for instance in storage_instances.values():
        instance.terminate()
    storage_instances.clear()
    
def exit2():
    terminateAll()
    sleep(1)
    sys.exit()
    
    
def _setPort(port):
    if port is None:
        global LAST_PORT
        port = LAST_PORT
        LAST_PORT += 1
    return port
    
    
def startStorage(shortkey, port=None, adminPort=None):
    port = _setPort(port)
    adminPort = _setPort(adminPort)
    if shortkey in storage_instances:
        raise Exception('%s already in running instaces' % shortkey)
    storage_instances[shortkey] = Popen(["./storageserver.py", "-p", str(port), "-a", str(adminPort), "-d", shortkey + ".bin"])
    print 'Created new storage service on port %d' % port
    sleep(3)
    connect("localhost", port, shortkey)
    
def ss(*args):
    startStorage(*args)
    
def connect(server, port, shortkey=None):
    if shortkey is None:
        shortkey = '%s:%d' % (server, port)
    if shortkey in connections:
        raise Exception('%s already in active connections, choose a new connection name' % shortkey)
    connections[shortkey] = SimpleStorageTestClient(server, port)
    
def disconnectAll():
    for conn in connections.values():
        conn.stop()
    connections.clear()
    
def write(shortkey, offset, data):
    if shortkey not in connections:
        raise Exception('%s does not exist' % shortkey)
    if not connections[shortkey].writeData(offset, data):
        del connections[shortkey]
    
    
def read(shortkey, offset, length):
    if shortkey not in connections:
        raise Exception('%s does not exist' % shortkey)
    if not connections[shortkey].readData(offset, length):
        del connections[shortkey] 
