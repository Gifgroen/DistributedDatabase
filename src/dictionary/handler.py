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

    def parsedMessage(self, msgData):
        requestMessage = DictionaryHeader()
        requestMessage.ParseFromString(msgData)
        
        log.msg("parsed message!")

        msg = self.protocol.factory.delegate.handleRequest(requestMessage)
        self.protocol.writeMsg(msg)
