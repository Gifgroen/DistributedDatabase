from generic.serverstatemachine import DataReceiver, HeaderLengthParser
from storage.contentreceiver import WriteContentReceiver


from generic.communication_pb2 import HashedStorageHeader, StorageHeader, StorageResponseHeader

from twisted.python import log

from hashlib import sha1
import sys, time

PRIVATE_HASH_KEY = "BLABLABLA"
HASH_EXPIRE_SECONDS = 30


class StorageHeaderParser(DataReceiver):
    def __init__(self, protocol, length):
        super(StorageHeaderParser, self).__init__(protocol)
        self.length = length
        self.header = HashedStorageHeader()
        
        
    def validateHash(self):
        if self.header.hashAlgorithm != HashedStorageHeader.SHA1:
            raise Exception("Unsupported hash")
        sha1hash = sha1(self.header.header.SerializeToString() + PRIVATE_HASH_KEY)
        log.msg('parsed hash: %s' % sha1hash.hexdigest())
        if self.header.hash != sha1hash.digest():
            raise Exception("Incorrect hash")
        timediff = int(time.time()) - self.header.header.requestTimestamp
        if timediff > HASH_EXPIRE_SECONDS:
            raise Exception("Hash key expired %d seconds" % timediff)
    
    # TODO refactor to seperate method
    def handleRead(self):
        log.msg('Parsed READ header, set state back to HeaderLengthParser, posting read task in queue')
        def diskReadFinished(offset, length, data):
            assert length == self.header.header.length
            
            log.msg('diskReadFinished: %s...' % data[:30])
            responseHeader = StorageResponseHeader()
            # TODO THIS SHOULD BE EASIER........ but copyfrom doesn't work
            responseHeader.header.operation = self.header.header.operation;
            responseHeader.header.offset = self.header.header.offset;
            responseHeader.header.length = self.header.header.length;
            responseHeader.header.requestTimestamp = self.header.header.requestTimestamp;

            responseHeader.status = StorageResponseHeader.OK
            self.protocol.writeMsg(responseHeader)
            self.protocol.writeRaw(data)
            log.msg('diskReadFinished finished writing')
        self.protocol.factory.server.db.pushRead(self.header.header.offset, self.header.header.length, diskReadFinished)
        
    def setMode(self):
        opp = self.header.header.operation
        if opp == StorageHeader.READ:
            self.handleRead()
            self.updateReceiver(HeaderLengthParser(self.protocol))
        elif opp == StorageHeader.WRITE:
            log.msg('Parsed WRITE header, start receiving content')
            self.updateReceiver(WriteContentReceiver(self.protocol, self.header))
        elif opp == StorageHeader.XOR_WRITE:
            log.msg('Parsed XOR_WRITE header, start receiving content')
            self.updateReceiver(XORWriteContentReceiver(self.protocol, self.header))
        else:
            raise Exception("Unkown operation")
            
    def handle(self):
        self.validateHash()
        self.setMode()
        
    def dataReceived(self):
        if len(self.protocol.buf) >= self.length:
            self.header.ParseFromString(self.popBytes(self.length))
            self.handle()
            return True
        return False
