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

    def sendMsg(self, msg):
        self.connection.sendMsg(msg)

    def readResponse(self):
        return self.connection.readMsg()

    def sendRequest(self, request):
        self.connection.sendMsg(request)

if __name__ == '__main__':
    print 'Connecting \n'
    dictCLI = DictionaryClient(HOST, PORT)
    
    rhead = DictionaryHeader()
    rhead.size = 59863
    rhead.key = 'foobar'
    rhead.operation = DictionaryHeader.ADD

    rhead2 = DictionaryHeader()
    rhead2.operation = DictionaryHeader.GET
    
    rhead3 = DictionaryHeader()
    rhead3.operation = DictionaryHeader.DELETE


    dictCLI.sendRequest(rhead)
    response = dictCLI.readResponse()
    print "RESPONSE: ", response, "\n"

    rhead2.key = response.key
    rhead3.key = response.key

    dictCLI.sendRequest(rhead2)
    response = dictCLI.readResponse()
    print "RESPONSE: ", response, "\n"

    dictCLI.sendRequest(rhead3)
    response3 = dictCLI.readResponse()
    print "RESPONSE: ", response, "\n"
    
    print 'closed'
    
    
