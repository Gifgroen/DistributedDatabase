from generic.communication_pb2 import DictionaryHeader # Dictheaders

from twisted.python import log

#from dictionary.server import LocationHandler

PROTOCOL_VERSION = 0b1

"""
Message handler that parses a message and delegates request
"""
class DictionaryRequestHandler():
    def __init__(self, protocol):
        self.protocol = protocol
        # LocationHandler must be shared among ALL requests
        # and not be created for every request!
        # So define it inside the server (in the factory).
        # self.delegate = LocationHandler()

    def parsedMessage(self, msgData):
        requestMessage = DictionaryHeader()
        requestMessage.ParseFromString(msgData)
        
        # TODO: Parse message
        log.msg("parsed message!")

        # TODO -> delegate request
        msg = self.protocol.factory.delegate.handleRequest(requestMessage)
        self.protocol.writeMsg(msg)
