
class FreeList:
    def __init__(self):
        self.memtable = {}  # contains 

    def allocSpace(self, sizeOfData):
        return {
            "hostname": "karsten.sorrybunch.nl", 
            "port": 65565, 
            "offset": 42,
            "length": sizeOfData,
        }
        
    def releaseSpace(self, host, port, offset, length):
        print "released", host, port, offset, length
