"""
The dictionary action delegate responsible for handling actual requests

All request messages return en LocationResponseHeader message
-> See layout in communication.proto
"""
from generic.communication_pb2 import DictionaryResponseHeader, DictionaryHeader
from dictionary.filetable import DictionaryTable

class LocationHandler:
    def __init__(self):
        self.requestHeader = None
        self.filetable = DictionaryTable()

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
        print self.requestHeader.key
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
        key = self.filetable.add(self.requestHeader.size)
        
        rhead = DictionaryResponseHeader()
        rhead.status = DictionaryResponseHeader.OK
        rhead.key = key
        rhead.locations.extend([])

        return rhead
        # TODO: look in freelist and set in filetable

        # TODO: Build proper response

    """
    Handle DELETE request
        -> input: key
        -> action: delete entry in filetable
        -> response: OK message
    """
    def handleDELETE(self):
        pass
        # TODO: delete from filetable and release in freelist

        # TODO: Build proper response
