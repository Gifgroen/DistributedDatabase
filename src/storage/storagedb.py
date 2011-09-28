from Queue import Queue, Empty
from threading import Lock, Thread

from twisted.internet import reactor
from twisted.python import log


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
        self.work_queue.put(('r', offset, length, callback, args))
    
    """
    Queue write request.
    This method writes all the data starting from
    the offset to disk.
    """
    def pushWrite(self, offset, data):
        self.work_queue.put(('w', offset, data))

    """
    Queue XOR write request.
    This method writes all the data starting from
    the offset to disk and XOR-es it with the current data.
    """
    def pushXORWrite(self, offset, data):
        self.work_queue.put(('x', offset, data))
        
    """
    Blocking request (with timeout) that tries to
    perform a piece of work that is inside the que.
    """
    def _handleOneRequest(self):
        try: # blocking for 1 second, after this Empty is thrown
            task = self.work_queue.get(True, 1)
            if task[0] == 'r':
                self._handleRead(*task[1:])
            elif task[0] == 'w':
                self._handleWrite(*task[1:])
            elif task[0] == 'x':
                self._handleXORWrite(*task[1:])
        except Empty:
            return
        
    """
    Handle read operation
    """
    def _handleRead(self, offset, length, callback, *args):
        self.dbFile.seek(offset)
        data = self.dbFile.read(length)
        log.msg(args)
        if args[0]:
            reactor.callFromThread(callback, offset, length, data, *args)
        else:
            reactor.callFromThread(callback, offset, length, data)
    
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
        for byte in data:
            self.dbFile.seek(offset)
            original = self.dbFile.read(1)
            self.dbFile.seek(offset)
            self.dbFile.write(byte ^ original)
            offset += 1
    
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
    
    a = StorageDatabase('testdb.bin')
    a.start()
    
    def doTest():
        msg = 'Dit is een test 12345'
        
        a.pushWrite(0, msg)
        a.pushWrite(1000, msg)
    
        a.pushRead(1000, len(msg), readFinished)
        a.pushRead(0, len(msg), readFinished)
    
    reactor.callLater(0, doTest)
    reactor.run()
    
