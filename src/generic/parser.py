from twisted.python import log

"""
TokenParser interface
"""
class TokenParser(object):
    def parse(self, byteStream, handler):
        raise NotImplementedError, "Token parser MUST implement parse method"

class VersionTokenParser(TokenParser):
    def parse(self, byteStream, handler):
        if byteStream.numBytesAvailable(1):
            handler.parsedVersionToken(byteStream.popByte())
            # we are finished reading, move to next token: header length
            return MessageLengthTokenParser()
        # there is not 1 byte available, so parser would block
        # we need to parse the next round again
        return None


class MessageLengthTokenParser(TokenParser):
    def parse(self, byteStream, handler):
        if byteStream.numBytesAvailable(1):
            msgLength = byteStream.popByte()
            handler.parsedMessageLengthToken(msgLength)
            # we are finished reading, move to next token: the Proto message
            return FixedLengthMessageParser(msgLength)
        return None


class FixedLengthMessageParser(TokenParser):
    def __init__(self, msgLength):
        self.msgLength = msgLength
        
    def parse(self, byteStream, handler):
        if byteStream.numBytesAvailable(self.msgLength):
            msgData = byteStream.popTokens(self.msgLength)
            # handleMessage might decide that a sequence 
            # of raw bytes must be parsed after the fixed
            # length message. If so, handleMessage will
            # return the length of this raw byte message
            rawByteLength = handler.parsedMessage(msgData)
            if rawByteLength and rawByteLength > 0:
                return FixedLengthRawBytesParser(rawByteLength)
            return MessageLengthTokenParser()
        return None # entire message can not be read yet
    
    
class FixedLengthRawBytesParser(TokenParser):
    def __init__(self, msgLength):
        self.bytesToParse = msgLength

    def parse(self, byteStream, handler):
        bytesRead = byteStream.popTokens(self.bytesToParse)
        self.bytesToParse -= len(bytesRead)
        handler.parsedRawBytes(bytesRead)
        if self.bytesToParse == 0: # reading raw bytes finished
            return MessageLengthTokenParser()
        return None # we have not finished yet, so block reading
            

"""
Parser class is responsible for handling the entire parse
functionality of the application.
It maintains the current stade in self.currentTokenParser
wich is an object with a .parse(byteStream, handler) method.
It will call the .parse() method of the current token parse
once if the Parser.parse() method is called, this methods
returns False if the Parser would block and thus needs more
data.
"""
class Parser(object):
    
    def __init__(self, handler):
        self.handler = handler
        # set initial token parser
        self.currentTokenParser = VersionTokenParser()

    """
    Pop and parse token(s) from byteStream. This methods calls
    the private parse* methods and sets the new state in
    self.currentParseFunction.
    Return False if the parser would block on the input stream.
    """
    def parse(self, byteStream):
        newTokenParser = self.currentTokenParser.parse(byteStream, self.handler)
        if newTokenParser is None:
            # current token parser blocked
            return False
        # token parser didn't block, so set (new) current token parser
        self.currentTokenParser = newTokenParser
        return True

