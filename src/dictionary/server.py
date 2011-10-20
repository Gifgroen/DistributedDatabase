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

        if self.requestHeader.operation == DictionaryHeader.GET:
            return self.handleGET()
        elif self.requestHeader.operation == DictionaryHeader.ADD:
            return self.handleADD()
        elif self.requestHeader.operation == DictionaryHeader.DELETE:
            return self.handleDELETE()

    """
    Handle GET request
        input    -> key
        action   -> search filetable for key entry
        response -> Location message (READ)
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

    """
    Handle ADD request
        input    -> size
        action   -> ADD entry in filetable
        response -> Location message (WRITE)
    """
    def handleADD(self):       
        # get space from freelist
        locs = self.fl.allocSpace(self.requestHeader.size)
        
        # generate a random key
        key = str(uuid.uuid4())
        for loc in locs:
            self.filetable.add(key, **loc)
        
        rhead = DictionaryResponseHeader()
        rhead.status = DictionaryResponseHeader.OK
        rhead.key = key
        rhead.locations.extend([])
        
        # if my responsibility
        #   -> store
        # else
        #   -> forward to responsible server

        return rhead


    """
    Handle DELETE request
        -> input: key
        -> action: delete entry in filetable
        -> response: OK message
    """
    def handleDELETE(self):
        # get the LocationEntry to free in freelist
        locs = self.filetable.get(self.requestHeader.key)

        # Release in freelist
        for loc in locs:
            self.fl.releaseSpace(**loc.toDict())
        
        rhead = DictionaryResponseHeader()
        rhead.status = DictionaryResponseHeader.OK
        
        # Delete from filetable
        status = self.filetable.delete(self.requestHeader.key)
        if status == False:
            rhead.status = DictionaryResponseHeader.NOT_EXISTING_KEY

        return rhead
