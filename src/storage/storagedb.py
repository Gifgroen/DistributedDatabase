from Queue import Queue, Empty
from threading import Lock, Thread

from twisted.internet import reactor
from twisted.python import log


def xorBytes(a, b):
    assert len(a) == len(b)
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(a, b))

def byteValue(bytes):
    return [ord(byte) for byte in bytes]

class StorageDatabase(object):
    
    """
    Create a StorageDatabase for a given filename.
    The file might use infinitly disk space, since the
    pushWrite request control the seeker.
    """
    def __init__(self, filename):
        self.filename = filename
        self.cont = False
        self.work_queue = Queue() # threadsafe queue
        reactor.addSystemEventTrigger('during', 'shutdown', self.stop)
        
    
    """
    Starts the database worker.
    Reads and writes will only be performed if this
    method is called.
    """
    def start(self):
        if self.cont:
            raise Exception("Already running")
        self.dbFile = open(self.filename, 'w+b')
        self.cont = True
        reactor.callInThread(self._workerFunction)
    
    """
    Stops the worker queue as soon as all the running
    tasks are finished.
    """
    def stop(self):
        self.cont = False
    
    """
    Queue a read request.
    The callback is called with the original offset
    and length, and the data.
    """
    def pushRead(self, offset, length, callback, *args):
        self.work_queue.put((self._handleRead,
            offset, length, callback, args))
    
    """
    Queue write request.
    This method writes all the data starting from
    the offset to disk.
    """
    def pushWrite(self, offset, data):
        self.work_queue.put((self._handleWrite, offset, data))

    """
    Queue XOR write request.
    This method writes all the data starting from
    the offset to disk and XOR-es it with the current data.
    This method is only used by RAID4 parity server
    P' = I XOR P.
    """
    def pushXORWrite(self, offset, data):
        self.work_queue.put((self._handleXORWrite, offset, data))
        
    """
    Queue XOR read request.
    This method reads all the from disk from offset
    to len(data) and XOR-es it with the data that
    is passed to the function.
    This method is used by the write server to send the
    XOR-update to the parity server. I = A' XOR A
    """
    def pushXORRead(self, offset, data, callback, *args):
        self.work_queue.put((self._handleXORRead,
            offset, data, callback, args))
    
    """
    Blocking request (with timeout) that tries to
    perform a piece of work that is inside the que.
    """
    def _handleOneRequest(self):
        try: # blocking for 1 second, after this Empty is thrown
            task = self.work_queue.get(True, 1)
            task[0](*task[1:])
        except Empty:
            return
        
    """
    Handle read operation
    """
    def _handleRead(self, offset, length, callback, args):
        self.dbFile.seek(offset)
        data = self.dbFile.read(length)
        reactor.callFromThread(callback, offset, length, data, *args)
    
    """
    Handle write operation
    """
    def _handleWrite(self, offset, data):
        self.dbFile.seek(offset)
        self.dbFile.write(data)
        
    """
    Handle XOR-write operation
    """
    def _handleXORWrite(self, offset, data):
        self.dbFile.seek(offset)
        original = self.dbFile.read(len(data))
        self.dbFile.seek(offset)
        self.dbFile.write(xorBytes(data, original))

    """
    Handle read operation
    """
    def _handleXORRead(self, offset, data, callback, args):
        self.dbFile.seek(offset)
        ondisk = self.dbFile.read(len(data))
        xored = xorBytes(ondisk, data)
        reactor.callFromThread(callback, offset, data, xored, *args)
    
    """
    Worker function that continues working until
    stop is called and the queue eventueally becomes
    empty.
    """
    def _workerFunction(self):
        while self.cont or not self.work_queue.empty():
            self._handleOneRequest()
        self.dbFile.close()


"""
For simple testing only...
"""
if __name__ == '__main__':
    import sys
    log.startLogging(sys.stdout)
    log.msg('Performing simple read/write tests')
    
    def readFinished(offset, length, data):
        log.msg('read from %d with length %d: %s' % (offset, length, data))
        
    def xorReadFinished(offset, length, data, expected):
        log.msg('read (%d): %s' % (len(data), byteValue(data)))
        log.msg('expected (%d): %s' % (len(expected), byteValue(expected)))
    
    a = StorageDatabase('testdb.bin')
    a.start()
    
    def doTest():
        msg = 'Dit is een test 12345'
        
        a.pushWrite(0, msg)
        a.pushWrite(1000, msg)
    
        a.pushRead(1000, len(msg), readFinished)
        a.pushRead(0, len(msg), readFinished)
        
        original = '1,2,3,4,5'
        new = 'a,b,c,d,e'
        result = xorBytes(new, original)
        
        a.pushWrite(100, original)
        a.pushXORWrite(100, new)
        a.pushRead(100, len(result), xorReadFinished, result)
    
    reactor.callLater(0, doTest)
    reactor.run()
    
