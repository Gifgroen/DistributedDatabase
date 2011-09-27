from generic.serverstatemachine import DataReceiver, HeaderLengthParser
from twisted.python import log
from generic.communication_pb2 import StorageResponseHeader

class WriteContentReceiver(DataReceiver):
    
    def __init__(self, protocol, header):
        super(WriteContentReceiver, self).__init__(protocol)
        self.header = header
        # maintain the state of the already written data:
        self.offset = header.header.offset
        self.restLength = header.header.length
    
    
    def handleReceivedBlock(self, offset, data):
        log.msg('write to db: %s at %d' % (data, offset))
        self.protocol.factory.server.db.pushWrite(self.offset, data)
        # TODO XOR and send the data to XOR-mate
        
        
    def itemUploadFinished(self):
        # set new receiver state in order to receive new requests
        log.msg('itemUploadFinished, change state back to HeaderLengthParser')
        self.updateReceiver(HeaderLengthParser(self.protocol))
        
        # send a reply to the
        responseHeader = StorageResponseHeader()
        
        #responseHeader.header.CopyFrom(self.header.header)
        # TODO THIS SHOULD BE EASIER........ but copyfrom doesn't work
        responseHeader.header.operation = self.header.header.operation;
        responseHeader.header.offset = self.header.header.offset;
        responseHeader.header.length = self.header.header.length;
        responseHeader.header.requestTimestamp = self.header.header.requestTimestamp;
        
        responseHeader.status = StorageResponseHeader.OK
        self.protocol.writeMsg(responseHeader)
    
    
    def dataReceived(self):
        # try to read at most header.length bytes, write to storage database
        data = self.popBytes(self.restLength)
        
        self.handleReceivedBlock(self.offset, data)
        
        self.offset += len(data)
        self.restLength -= len(data)
        
        if self.restLength == 0:
            self.itemUploadFinished()
            #return False
        return True
    
    

class XORWriteContentReceiver(DataReceiver):

    def __init__(self, protocol, header):
        super(XORWriteContentReceiver, self).__init__(protocol)
        #self.header = header
    
    def dataReceived(self):
        raise Exception("XOR WRITE Not implemented yet...")
        
    