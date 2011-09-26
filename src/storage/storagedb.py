from Queue import Queue, Empty
from threading import Lock, Thread

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
        t = Thread(target = self._workerFunction)
        t.start()
    
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
    def pushRead(self, offset, length, callback):
        self.work_queue.put((offset, length, callback))
    
    """
    Queue write request.
    This method writes all the data starting from
    the offset to disk.
    """
    def pushWrite(self, offset, data):
        self.work_queue.put((offset, data))
    
    """
    Blocking request (with timeout) that tries to
    perform a piece of work that is inside the que.
    """
    def _handleOneRequest(self):
        try: # blocking for 10 seconds, after this Empty is thrown
            args = self.work_queue.get(True, 10)
            if (len(args) == 3):
                self._handleRead(*args)
            else: # len(args) == 2
                self._handleWrite(*args)
        except Empty:
            return
        
    """
    Handle read operation
    """
    def _handleRead(self, offset, length, callback):
        self.dbFile.seek(offset)
        data = self.dbFile.read(length)
        callback(offset, length, data)
    
    """
    Handle write operation
    """
    def _handleWrite(self, offset, data):
        self.dbFile.seek(offset)
        self.dbFile.write(data)
    
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
    print 'Performing simple read/write tests'
    print '-'*50
    
    def readFinished(offset, length, data):
        print 'read from %d with length %d: %s' % (offset, length, data)
    
    a = StorageDatabase('testdb.bin')
    a.start()
    msg = 'Dit is een test 12345'
    a.pushWrite(0, msg)
    a.pushWrite(1000, msg)
    
    a.pushRead(1000, len(msg), readFinished)
    a.pushRead(0, len(msg), readFinished)
    
    a.stop()
    