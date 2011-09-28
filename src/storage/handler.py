from generic.communication_pb2 import HashedStorageHeader, StorageHeader, StorageResponseHeader

from twisted.python import log

from hashlib import sha1
import time

PROTOCOL_VERSION = 0b1

PRIVATE_HASH_KEY = "BLABLABLA"
HASH_EXPIRE_SECONDS = 30


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
        
    def parsedVersionToken(self, version):
        log.msg("parsedVersionToken(%d)" % version)
        if PROTOCOL_VERSION != version:
            raise Exception("Wrong protocol version")
        
    def parsedMessageLengthToken(self, length):
        log.msg("parsedMessageLengthToken(%d)" % length)
        if length == 0:
            raise Exception("Received 0 length message")
            
    def _validateHash(self, signedHeader):
        if signedHeader.hashAlgorithm != HashedStorageHeader.SHA1:
            raise Exception("Unsupported hash")
        sha1hash = sha1(signedHeader.header.SerializeToString() + PRIVATE_HASH_KEY)
        log.msg('parsed hash: %s' % sha1hash.hexdigest())
        if signedHeader.hash != sha1hash.digest():
            raise Exception("Incorrect hash")
        timediff = int(time.time()) - signedHeader.header.requestTimestamp
        if timediff > HASH_EXPIRE_SECONDS:
            raise Exception("Hash key expired %d seconds" % timediff)
        
    def _handleStorgeHeader(self, header):
        opp = header.operation
        length = header.length
        if opp == StorageHeader.READ:
            log.msg('Parsed READ header,  read operation')
            self.db.pushRead(header, self.diskReadFinished) # TOOOOOOOOOOOOOOOODOOOOOOOOOOOOOOOO
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
    TODO: fix multiple read bug... header should be argument of diskReadFinished
    """
    def diskReadFinished(header, data):
        log.msg('diskReadFinished: %s...' % data[:30])
        responseHeader = StorageResponseHeader()
        
        # TODO THIS SHOULD BE EASIER........ but header.copyfrom doesn't work
        responseHeader.header.operation = header.operation;
        responseHeader.header.offset = header.offset;
        responseHeader.header.length = header.length;
        responseHeader.header.requestTimestamp = header.requestTimestamp;

        responseHeader.status = StorageResponseHeader.OK
        self.protocol.writeMsg(responseHeader)
        self.protocol.writeRaw(data)
        log.msg('diskReadFinished finished writing')
        
    def parsedMessage(self, msgData):
        signedHeader = HashedStorageHeader()
        signedHeader.ParseFromString(msgData)
        self._validateHash(signedHeader)
        return self._handleStorgeHeader(signedHeader)
        
    def parsedRawBytes(self, bytes): # doesn't have to be implemented by dictionary service
        log.msg("Received %d raw bytes" % len(bytes))
        # TODO: send to storage or XOR and send to storage
        
        
        
