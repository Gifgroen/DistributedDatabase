def getFreeSpace(sizeOfData):
    return {
        "hostname": "karsten.sorrybunch.nl", 
        "port": 65565, 
        "offset": 42,
        "length": sizeOfData,
        "key": "0xDEADBEEF"
    }
    
def releaseSpace(loc):
    print "released", loc
    return True
