"""
The dictionary action delegate responsible for handling actual requests

All request messages return en LocationResponseHeader message
-> See layout in communication.proto
"""
from generic.communication_pb2 import DictionaryReponseHeader

class LocationHandler:
    def __init__(self):
        pass

    def handleRequest(self, dictResponse):
        pass

    """
    Handle ADD request
        input    -> size
        action   -> ADD entry in filetable
        response -> Location message (WRITE)
    """
    def handleAdd():
        pass

    """
    Handle DELETE request
        -> input: key
        -> action: delete entry in filetable
        -> response: OK message
    """
    def handleDelete():
        pass

    """
    Handle GET request
        input    -> key
        action   -> search filetable for key entry
        response -> Location message (READ)
    """
    def handleGet():
        pass
