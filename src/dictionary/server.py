"""
The dictionary action delegate responsible for handling actual requests

All request messages return en LocationResponseHeader message
-> See layout in communication.proto
"""
from generic.communication_pb2 import DictionaryResponseHeader, DictionaryHeader

from dictionary.filetable import DictionaryTable

from freelist.spacetable import FreeList

import uuid

class LocationHandler:
    def __init__(self):
        self.requestHeader = None
        self.filetable = DictionaryTable()
        self.fl = FreeList()

    def handleRequest(self, header):
        self.requestHeader = header

        # These actions return Status and redirect in case of ADD, other two return None as redirect
        if self.requestHeader.operation == DictionaryHeader.HEARTBEAT:
            return self.handleHeartbeat()
        elif self.requestHeader.operation == DictionaryHeader.GET:
            return self.handleGET()
        elif self.requestHeader.operation == DictionaryHeader.ADD:
            return self.handleADD()
        elif self.requestHeader.operation == DictionaryHeader.DELETE:
            return self.handleDELETE()

    """
    It is possible that we get heartbeat from the manager, we respond with a OK
    """
    def handleHeartbeat(self):
        rhead = DictionaryResponseHeader()
        rhead.status = DictionaryResponseHeader.OK
        return rhead

    """
    Handle GET request
        input    -> key
        action   -> search filetable for key entry
        response -> Location message (READ) + redirect (not necessary here)
    """
    def handleGET(self):
        locs = self.filetable.get(self.requestHeader.key)

        rhead = DictionaryResponseHeader()
        if not locs:
            rhead.status = DictionaryResponseHeader.NOT_EXISTING_KEY
        else:
            rhead.status = DictionaryResponseHeader.OK
            for loc in locs:
                rhead.locations.extend([loc.toReadMessage()])

        return rhead

    def add(self):
        # get space from freelist
        locs = self.fl.allocSpace(self.requestHeader.size)
        
        generatedKey = False
        if self.requestHeader.key != "":
            # use the existing key
            key = self.requestHeader.key
        else:
            # generate a random key
            key = str(uuid.uuid4())

        for loc in locs:
            self.filetable.add(key, **loc)
            
        return key

    """
    Handle ADD request
        input    -> size
        action   -> ADD entry in filetable
        response -> Location message (WRITE) + redirect (if necessary)
    """
    def handleADD(self):
        rhead = DictionaryResponseHeader()
        rhead.locations.extend([])

        key = self.add()
        
        rhead.status = DictionaryResponseHeader.OK
        rhead.key = key
        return rhead


    def delete(self):
        # get the LocationEntry to free in freelist
        locs = self.filetable.get(self.requestHeader.key)

        # Release in freelist
        for loc in locs:
            self.fl.releaseSpace(**loc.toDict())
        
        # Delete from filetable
        status = self.filetable.delete(self.requestHeader.key)
        
        return status

    """
    Handle DELETE request
        -> input: key
        -> action: delete entry in filetable
        -> response: OK message + redirect (not necessary here)
    """
    def handleDELETE(self):
        rhead = DictionaryResponseHeader()
        rhead.locations.extend([])
        rhead.status = DictionaryResponseHeader.OK
    
        # delete the current key
        status = self.delete()
        if status == False:
            rhead.status = DictionaryResponseHeader.NOT_EXISTING_KEY
        
        return rhead


