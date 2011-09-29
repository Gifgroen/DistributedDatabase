from generic.communication_pb2 import DictionaryReponseHeader # Dictheaders

from twisted.python import log

from dictionary.server import LocationHandler

PROTOCOL_VERSION = 0b1

"""
Message handler that parses a message and delegates request
"""
class DictionaryRequestHandler():
    def __init__(self, protocol):
        self.protocol = protocol
        self.delegate = LocationHandler()

    def parsedMessage(self, msgData):
        requestMessage = HashedStorageHeader()
        requestMessage.ParseFromString(msgData)
        
        # TODO: Parse message
        log.msg("parsed message!")

        # TODO -> delegate request
        self.delegate.handleRequest(requestMessage)
