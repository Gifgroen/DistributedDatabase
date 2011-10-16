"""
Import this module in a python terminal
"""

import sys, traceback
from time import sleep
from storageclient import SimpleStorageTestClient
from subprocess import Popen

LAST_PORT = 8080

storage_instances = {} #shortkey -> Popen
parity_instances = {} #shortkey -> Popen
connections = {} #shortkey -->SimpleStorageTestClient

def exit2():
    for instance in storage_instances.values():
        instance.terminate()
    for instance in parity_instances.values():
        instance.terminate()
    sleep(1)
    sys.exit()
    
    
def _setPort(port):
    if port is None:
        global LAST_PORT
        port = LAST_PORT
        LAST_PORT += 1
    return port
    
    
def startStorage(shortkey, xor_host, xor_port, port=None):
    port = _setPort(port)
    if shortkey in storage_instances:
        raise Exception('%s already in running instaces' % shortkey)
    storage_instances[shortkey] = Popen(["./storageserver.py", "-p", str(port), "-d", shortkey + ".bin", "--xor_host", xor_host, "--xor_port", str(xor_port)])
    print 'Created new storage service on port %d' % port
    sleep(3)
    connect("localhost", port, shortkey)
    
def ss(*args):
    startStorage(*args)
    
def startParityStorage(shortkey, port=None):
    port = _setPort(port)
    if shortkey in parity_instances:
        raise Exception('%s already in running instaces' % shortkey)
    parity_instances[shortkey] = Popen(["./storageserver.py", "-p", str(port), "-d", shortkey + ".bin"])
    print 'Created new parity service on port %d' % port
    sleep(3)
    connect("localhost", port, shortkey)

def sps(shortkey):
    startParityStorage(shortkey)
    
    
def connect(server, port, shortkey):
    if shortkey is None:
        shortkey = server 
    if shortkey in connections:
        raise Exception('%s already in active connections, choose a new connection name' % shortkey)
    connections[shortkey] = SimpleStorageTestClient(server, port)
    
    
def write(shortkey, offset, data):
    if shortkey not in connections:
        raise Exception('%s does not exist' % shortkey)
    connections[shortkey].writeData(offset, data)
    
    
def read(shortkey, offset, length):
    if shortkey not in connections:
        raise Exception('%s does not exist' % shortkey)
    return connections[shortkey].readData(offset, length)
    
"""
helper function
"""
    
def xorBytes(a, b):
    assert len(a) == len(b)
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(a, b))
    
    
    
msg1 = "Hello World!"
msg2 = "Blablablablaaaa"
def setup():
    sps('xor1')
    sleep(1)
    ss('server1', 'localhost', 8080)
    sleep(1)
    ss('server2', 'localhost', 8080)
    sleep(3)
    write('server1', 0, msg1)
    print read('xor1', 0, len(msg1)) # xor result of smallest message
    
    write('server2', 0, msg2)
    print read('server1', 0, len(msg1))
    print read('server2', 0, len(msg2))
    print read('xor1', 0, len(msg1)) # xor result of smallest message
    
