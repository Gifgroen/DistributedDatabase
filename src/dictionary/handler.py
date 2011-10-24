from generic.communication_pb2 import DictionaryHeader # Dictheaders

from twisted.python import log

PROTOCOL_VERSION = 0b1

"""
Message handler that parses a message and delegates request
"""
class DictionaryRequestHandler():
    def __init__(self, protocol):
        self.protocol = protocol
        
    def status(self):
        print "Done..."

    def putReplicaUpdates(self, msg):
        """
         start the replicaNotifier() it might have been stoppedd when it's empty.
         -> We know that it might be filled later
        """
        try:
            self.protocol.factory.replicaNotifier.start()
        except:
            print "Already running!?"
        # Put replication message in Queue of Dictserver
        for server in self.protocol.factory.replicaList:
            self.protocol.factory.replicaNotifier.sendReplicaUpdate(server['host'], server['port'], redirect, status)
        

    def parsedMessage(self, msgData):
        print "PARSEDD"
        requestMessage = DictionaryHeader()
        requestMessage.ParseFromString(msgData)
        
        log.msg("parsed dict message!")

        status, redirect = self.protocol.factory.delegate.handleRequest(requestMessage)
    
        print status
    
        # Respond with status
        self.protocol.writeMsg(status)
        if redirect != None and self.protocol.factory.replicaList != []:
            self.putReplicaUpdates(redirect)

        

