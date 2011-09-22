#!/usr/bin/env python
import sys, time
from hashlib import sha1
from struct import unpack

from twisted.python import log
from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory, Protocol

from communication_pb2 import HashedStorageHeader, StorageHeader

PRIVATE_HASH_KEY = "BLABLABLA"
HASH_EXPIRE_SECONDS = 30

PROTOCOL_VERSION = 0b1

STRUCT_BYTE = "!B"

"""
Interface for DataReceiver class
Derived classes of this type will be called if new data is available
in the buffer of the BinaryDataReceiverProtocol.
In fact, this is just a state machine for that class.
It is required that the DataReceiver changes the dataReceiver of
protocol, or that it makes the buffer entirely empty or that it
return False to prevent endless loops.

Note: never use this interface, it just clears the buffer....
"""
class DataReceiver(object):
    
    def __init__(self, protocol):
        self.protocol = protocol
        
    def popByte(self):
        res = self.protocol.buf[0]
        self.protocol.buf = self.protocol.buf[1:]
        return res
        
    def updateReceiver(self, receiver):
        self.protocol.dataReceiver = receiver
    
    """
    Protocol has data received
    Returns if True DataReceiver has read enough data
    """
    def dataReceived(self):
        raise NotImplementedError, "Implement a dataReceived method"

class ProtocolVersionChecker(DataReceiver):
    def dataReceived(self):
        if unpack(STRUCT_BYTE, self.popByte())[0] != PROTOCOL_VERSION:
            raise Exception("Wrong protocol version")
        self.updateReceiver(HeaderLengthParser(self.protocol))
        return True

class HeaderLengthParser(DataReceiver):
    def dataReceived(self):
        length = unpack(STRUCT_BYTE, self.popByte())[0]
        if length == 0:
            raise Exception("Received zero length header")
        self.updateReceiver(HeaderParser(self.protocol, length))
        return True
        
class HeaderParser(DataReceiver):
    def __init__(self, protocol, length):
        super(HeaderParser, self).__init__(protocol)
        self.length = length
        # TODO make flexibible for multiple implementations
        self.header = HashedStorageHeader()
        
    def validateHash(self):
        if self.header.hashAlgorithm != HashedStorageHeader.SHA1:
            raise Exception("Unsupported hash")
        sha1hash = sha1(self.header.header.SerializeToString() + PRIVATE_HASH_KEY)
        print sha1hash.hexdigest()
        if self.header.hash != sha1hash.digest():
            raise Exception("Incorrect hash")
        timediff = int(time.time()) - self.header.header.requestTimestamp
        if timediff > HASH_EXPIRE_SECONDS:
            raise Exception("Hash key expired %d seconds" % timediff)
        
    def setMode(self):
        opp = self.header.header.operation
        if opp == StorageHeader.READ:
            print "read"
        elif opp == StorageHeader.WRITE:
            print "write"
        elif opp == StorageHeader.XOREDWRITE:
            print "xoredwrite"
        else:
            raise Exception("Unkown operation")
            
    def handle(self):
        self.validateHash()
        self.setMode()
        
    def dataReceived(self):
        if len(self.protocol.buf) >= self.length:
            self.header.ParseFromString(self.protocol.buf[:self.length])
            self.protocol.buf = self.protocol.buf[self.length:]
            self.handle()
            return True
        return False

class BinaryDataReceiverProtocol(Protocol):
    
    def __init__(self):
        self.buf = ""
        self.dataReceiver = ProtocolVersionChecker(self)
        
    def connectionMade(self):
        self.factory.numProtocols += 1
        print('Connect... activive connections: %d' % self.factory.numProtocols)
        #if self.factory.numProtocols > 100: # or other check, memory in use or something like that
        #    self.transport.write("Too many connections, try later") 
        #    self.transport.loseConnection()
        
    def connectionLost(self, reason):
        self.factory.numProtocols -= 1
        print('Disconnect... activive connections: %d' % self.factory.numProtocols)
            
    def dataReceived(self, data):
        self.buf += data # append new data to buffer
        while self.buf and self.dataReceiver.dataReceived():
            pass
        
if __name__ == '__main__':
    log.startLogging(sys.stdout)
    factory = Factory()
    factory.numProtocols = 0
    factory.protocol = BinaryDataReceiverProtocol
    #reactor.listenTCP(7777, factory)
    reactor.listenSSL(7777, factory,
                      ssl.DefaultOpenSSLContextFactory(
            'sslcert/key.pem', 'sslcert/cert.pem'))
    reactor.run()
    # TODO: fix something for connection timeout
    