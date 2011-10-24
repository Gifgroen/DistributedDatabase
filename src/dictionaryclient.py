#!/usr/bin/env python
import sys, ssl, socket
from struct import pack, unpack

from generic.communication_pb2 import DictionaryHeader, DictionaryResponseHeader
from generic.protobufconnection import *

HOST = 'localhost'    # The remote host
PORT = 8989           # The same port as used by the server

STRUCT_BYTE = "!B"

class DictionaryClient(object):
    def __init__(self, host, port):
        self.connection = BlockingProtoBufConnection(DictionaryResponseHeader)
        self.connection.start(host, port)
        self.key = ""

    def sendMsg(self, msg):
        self.connection.sendMsg(msg)

    def readMsg(self):
        return self.connection.readMsg()

    def sendRequest(self, request):
        self.connection.sendMsg(request)
        
    def getKey(self):
        return self.key
        
    def sendADD(self, sizeOfData):
        req = DictionaryHeader()
        req.size = sizeOfData
        req.key = "foobar"  # REMOVE AFTER TESTING, RESULTS IN BAD BEHAVIOUR IN PRODUCTION ENV
        req.operation = DictionaryHeader.ADD
        
        self.sendRequest(req)
        response = self.readMsg()
        self.key = response.key
        
        return response
        
    def sendGET(self, key):
        req = DictionaryHeader()
        req.operation = DictionaryHeader.GET
        req.key = key

        self.sendRequest(req)
        return self.readMsg()
        
    def sendDELETE(self, key):
        req = DictionaryHeader()
        req.operation = DictionaryHeader.DELETE
        req.key = key

        self.sendRequest(req)
        return self.readMsg()
        

if __name__ == '__main__':
    print 'Connecting \n'
    dictCLI = DictionaryClient(HOST, PORT)
    
    size = 59863
    print dictCLI.sendADD(size)
    print dictCLI.sendGET(dictCLI.getKey())
    print dictCLI.sendDELETE(dictCLI.getKey())
   

    print 'closed'
    
    
