from generic.communication_pb2 import HashedStorageHeader, StorageHeader, StorageResponseHeader

from twisted.python import log

from hashlib import sha1
import time

PRIVATE_HASH_KEY = "BLABLABLA"
HASH_EXPIRE_SECONDS = 30

"""
Helper function to copy the entire header data from
a given header to another.
The protobuf python library doesn't support this by
default?
"""
def copyHeaderData(fromHeader, toHeader):
    toHeader.operation = fromHeader.operation;
    toHeader.offset = fromHeader.offset;
    toHeader.length = fromHeader.length;
    toHeader.requestTimestamp = fromHeader.requestTimestamp;
    

"""
Request handler for extrnal storage requests, every connection
has its own handler, so it is save to store private properties
per connection.
The database is shared accros other StorageRequestHandlers.
"""
class StorageRequestHandler():
    
    def __init__(self, protocol):
        self.protocol = protocol
        self.db = protocol.factory.db
        self.signedHeader = None
        self.currentWriteOffset = 0
            
    def _validateHash(self):
        if self.signedHeader.hashAlgorithm != HashedStorageHeader.SHA1:
            raise Exception("Unsupported hash")
        sha1hash = sha1(self.signedHeader.header.SerializeToString() + PRIVATE_HASH_KEY)
        log.msg('parsed hash: %s' % sha1hash.hexdigest())
        if self.signedHeader.hash != sha1hash.digest():
            raise Exception("Incorrect hash")
        timediff = int(time.time()) - self.signedHeader.header.requestTimestamp
        if timediff > HASH_EXPIRE_SECONDS:
            raise Exception("Hash key expired %d seconds" % timediff)
        
    def _handleStorgeHeader(self):
        header = self.signedHeader.header
        opp = header.operation
        length = header.length
        if opp == StorageHeader.READ:
            log.msg('Parsed READ header,  read operation')
            self.db.pushRead(header.offset, header.length, self.diskReadFinished, header)
            return 0 # we don't want to receive any raw data
        elif opp == StorageHeader.WRITE:
            log.msg('Parsed WRITE header, waiting for %d bytes' % length)
            return length
        elif opp == StorageHeader.XOR_WRITE:
            log.msg('Parsed XOR_WRITE header, waiting for %d bytes' % length)
            return length
        raise Exception("Unkown operation")
    
    """
    Signaled by database if read data is finished
    Important note: this function is called from the disk r/w
    thread, so in the meanwhile it is theoretical possible that
    self.signedHeader is replaced with a new operation. This 
    means that only parameters might be used.
    self.protocol.writeMsg can be called since only one thread
    is allowed to execute this.
    """
    def diskReadFinished(self, offset, length, data, header):
        log.msg('diskReadFinished: %s...' % data[:30])
        self._sendACK(header)
        self.protocol.writeRaw(data)
        
    """
    Send storage acknowledge to client
    """
    def _sendACK(self, header):
        responseHeader = StorageResponseHeader()
        copyHeaderData(header, responseHeader.header)
        responseHeader.status = StorageResponseHeader.OK
        self.protocol.writeMsg(responseHeader)
        
    """
    Message received by parser
    """
    def parsedMessage(self, msgData):
        self.signedHeader = HashedStorageHeader()
        self.signedHeader.ParseFromString(msgData)
        self.currentWriteOffset = 0
        self._validateHash()
        return self._handleStorgeHeader()
        
    def _sendXORUpdate(self, bytes): # what if is not received by other peer?
        pass # TODO
        
    def parsedRawBytes(self, bytes): # doesn't have to be implemented by dictionary service
        log.msg("Received %d raw bytes" % len(bytes))
        header = self.signedHeader.header
        if header.operation == StorageHeader.WRITE:
            log.msg('Write raw bytes of length %d' % len(bytes))
            self.db.pushWrite(self.currentWriteOffset, bytes)
            self._sendXORUpdate(bytes)
        elif header.operation == StorageHeader.XOR_WRITE:
            log.msg('Write the XORED result raw bytes of length %d' % len(bytes))
            self.db.pushXORWrite(self.currentWriteOffset, bytes)
        self.currentWriteOffset += len(bytes)
        if self.currentWriteOffset == header.offset + header.length:
            self._sendACK(self.signedHeader.header)
