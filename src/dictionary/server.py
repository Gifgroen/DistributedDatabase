"""
The dictionary action delegate responsible for handling actual requests

All request messages return en LocationResponseHeader message
-> See layout in communication.proto
"""
from generic.communication_pb2 import DictionaryResponseHeader, HashedStorageHeader, StorageHeader, DictionaryHeader
from dictionary.filetable import DictionaryTable

class LocationHandler:
    def __init__(self):
        self.requestHeader = None
        self.filetable = DictionaryTable()

    def handleRequest(self, header):
        self.requestHeader = header

        rmsg = None
        if self.requestHeader.operation == DictionaryHeader.GET:
            rmsg = self.handleGET()
        elif self.requestHeader.operation == DictionaryHeader.ADD:
            rmsg = self.handleADD()
        elif self.requestHeader.operation == DictionaryHeader.DELETE:
            rmsg = self.handleDELETE()
        return rmsg

    """
    Handle GET request
        input    -> key
        action   -> search filetable for key entry
        response -> Location message (READ)
    """
    def handleGET(self):
        locs = self.filetable.get(self.request.key)
        
        for loc in locs:
            if loc:
                pass
            
        # TODO: Build proper response

    """
    Handle ADD request
        input    -> size
        action   -> ADD entry in filetable
        response -> Location message (WRITE)
    """
    def handleADD(self):
        # TODO: look in freelist and set in filetable

        # TODO: Build proper response

    """
    Handle DELETE request
        -> input: key
        -> action: delete entry in filetable
        -> response: OK message
    """
    def handleDELETE(self):
        # TODO: delete from filetable and release in freelist

        # TODO: Build proper response
