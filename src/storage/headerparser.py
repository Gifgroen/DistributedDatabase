from generic.serverstatemachine import DataReceiver, HeaderLengthParser
from storage.contentreceiver import WriteContentReceiver

class StorageHeaderParser(DataReceiver):

    
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
        

            
        
