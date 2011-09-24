from generic.serverstatemachine import DataReceiver

from generic.communication_pb2 import HashedStorageHeader, StorageHeader

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
        
    def setMode(self):
        opp = self.header.header.operation
        if opp == StorageHeader.READ:
            print "read"
        elif opp == StorageHeader.WRITE:
            print "write"
        elif opp == StorageHeader.XOR_WRITE:
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