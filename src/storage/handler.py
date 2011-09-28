from generic.communication_pb2 import HashedStorageHeader#, StorageHeader, StorageResponseHeader

from twisted.python import log

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
        
    def parsedMessage(self, msgData):
        signedHeader = HashedStorageHeader()
        signedHeader.ParseFromString(msgData)
        log.msg("parsed message! wants to receive %d bytes" % signedHeader.header.length)
        # TODO
        return signedHeader.header.length
        
        
    def parsedRawBytes(self, bytes): # doesn't have to be implemented by dictionary service
        log.msg("Received %d raw bytes" % len(bytes))
