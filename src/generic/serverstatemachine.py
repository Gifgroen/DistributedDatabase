from struct import unpack, pack

from twisted.python import log
from twisted.internet.protocol import Protocol

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

Note: never use this interface itself
"""
class DataReceiver(object):
    
    def __init__(self, protocol):
        self.protocol = protocol
        
    def popByte(self):
        return self.popBytes(1)
        
    def updateReceiver(self, receiver):
        self.protocol.dataReceiver = receiver
        
    def popBytes(self, length):
        res = self.protocol.buf[:length]
        self.protocol.buf = self.protocol.buf[length:]
        return res
    
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
        self.updateReceiver(self.protocol.factory.headerParserClass(self.protocol, length))
        return True


class BinaryDataReceiverProtocol(Protocol):
    
    def __init__(self):
        self.buf = ""
        self.dataReceiver = ProtocolVersionChecker(self)
        
    def writeRaw(self, rawData):
        # TODO fix mutex?
        self.transport.write(rawData)
        
    def writeMsg(self, protoBufMsg):
        # TODO write mutex / queue?
        msgData = protoBufMsg.SerializeToString()
        self.transport.write(pack(STRUCT_BYTE, len(msgData)))
        log.msg('Send protoBufMsg of length %d to client.' % len(msgData))
        self.transport.write(msgData)
        
        
    def connectionMade(self):
        self.factory.connections.append(self)
        log.msg('New connection, total activive connections: %d' % len(self.factory.connections))
        if len(self.factory.connections) > 100: # or check memory in use or something like that
            self.transport.write("Too many connections, try later") 
            self.transport.loseConnection()
        
    def connectionLost(self, reason):
        # TODO: maybe more efficient connection list...
        self.factory.connections.remove(self)
        log.msg('Connection disconnected, total activive connections: %d' % len(self.factory.connections))
        
    def dataReceived(self, data):
        self.buf += data # append new data to buffer
        while self.buf and self.dataReceiver.dataReceived():
            pass

