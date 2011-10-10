from twisted.python import log


# TODO

class XORPartnerConnection(object):
    def __init__(self, serverLocation):
        self.serverLocation = serverLocation
        self.sendQueue = None#TODO
        
    def sendXORUpdate(self, offset, bytes, callback):
        pass # TODO