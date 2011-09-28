from generic.communication_pb2 import HashedLocationHeader # Dictheaders

from twisted.python import log

from dictionary import LocationHandler

PROTOCOL_VERSION = 0b1

"""
Message handler that parses a message and delegates request
"""
class DictionaryRequestHandler():
    def __init__(self, protocol):
        self.protocol = protocol
        self.delegate = LocationHandler()

    def parsedVersionToken(self, version):
        log.msg("parsedVersionToken(%d)" % version)
        if PROTOCOL_VERSION != version:
            raise Exception("Wrong protocol version")

    def parsedMessageLengthToken(self, length):
        log.msg("parsedMessageLengthToken(%d)" % length)
        if length == 0:
            raise Exception("Received 0 length message")

    def parsedMessage(self, msgData):
        # locationMessage = HashedLocationHeader()
        # locationMessage.ParseFromString(msgData)

        # log.msg("parsed message! TODO")
        # TODO: Parse message -> delegate request
