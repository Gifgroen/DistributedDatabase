"""
The dictionary action delegate responsible for handling actual requests

All request messages return en LocationResponseHeader message
-> See layout in communication.proto
"""
from generic.communication_pb2 import DictionaryResponseHeader, HashedStorageHeader, StorageHeader
from dictionary.filetable import DictionaryTable

class LocationHandler:
    def __init__(self):
        self.requestHeader = None
        self.filetable = DictionaryTable()

    def handleRequest(self, dictResponse):
        self.requestHeader = dictResponse

        rmsg = None
        if self.requestHeader.header.operation == StorageHeader.READ:
            rmsg = self.handleGET()
        elif self.requestHeader.header.operation == StorageHeader.WRITE:
            rmsg = self.handleADD()
        else:
            rmsg = self.handleDELETE()
        return rmsg

    """
    Handle ADD request
        input    -> size
        action   -> ADD entry in filetable
        response -> Location message (WRITE)
    """
    def handleADD(self):
        # TODO: look in freelist and set in filetable

        rhead = DictionaryResponseHeader()
        
        # TODO: Build proper response
        print dir(rhead.headers)
        rhead.headers.extend([self.requestHeader])
        rhead.hosts.append("localhost")
        rhead.ports.append(4242)

        return rhead

    """
    Handle DELETE request
        -> input: key
        -> action: delete entry in filetable
        -> response: OK message
    """
    def handleDELETE(self):
        # TODO: delete from filetable and release in freelist

        # TODO: Build proper response
        rhead = DictionaryResponseHeader()
        rhead.headers.extend([self.requestHeader])
        rhead.hosts.append("localhost")
        rhead.ports.append(4242)

        return rhead

    """
    Handle GET request
        input    -> key
        action   -> search filetable for key entry
        response -> Location message (READ)
    """
    def handleGET(self):
        # TODO: get location from filetable

        # TODO: Build proper response
        rhead = DictionaryResponseHeader()
        rhead.headers.extend([self.requestHeader])
        rhead.hosts.append("localhost")
        rhead.ports.append(4242)
        
        return rhead
