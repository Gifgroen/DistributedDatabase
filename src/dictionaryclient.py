#!/usr/bin/env python
import sys, ssl, socket
from struct import pack, unpack

from generic.communication_pb2 import HashedStorageHeader, StorageHeader, DictionaryHeader, DictionaryResponseHeader

HOST = 'localhost'    # The remote host
PORT = 8989           # The same port as used by the server

STRUCT_BYTE = "!B"

def readNBytes(ssl_sock, numBytes):
    msgData = ''
    while len(msgData) != numBytes:
        restLength = numBytes - len(msgData)
        received = ssl_sock.read(restLength)
        msgData = msgData + received
    return msgData

def sendMsg(ssl_sock, msg):
    msgData = msg.SerializeToString()
    assert len(msgData) < 256
    ssl_sock.send(pack(STRUCT_BYTE, len(msgData)))
    ssl_sock.send(msgData)


def readResponse(ssl_sock):
    responseHeaderLength = unpack(STRUCT_BYTE, readNBytes(ssl_sock, 1))[0]
    responseHeaderData = readNBytes(ssl_sock, responseHeaderLength)
    responseHeader = DictionaryResponseHeader()
    responseHeader.ParseFromString(responseHeaderData)

    return responseHeader

def sendADDRequest(ssl_sock, head):
    # send ADD message
    sendMsg(ssl_sock, head)

def sendGETRequest(ssl_sock, head):
    # send GET message
    sendMsg(ssl_sock, head)


def sendDELETERequest(ssl_sock, key):
    # construct DELETE message
    rhead = createRequestHeader(DictionaryHeader.DELETE, key)
    sendMsg(ssl_sock, rhead)


if __name__ == '__main__':
    print 'Creating socket \n'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(s, ca_certs="sslcert/cert.pem", cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_SSLv23)

    print 'Connecting \n'
    ssl_sock.connect((HOST, PORT))
    # protocol version
    ssl_sock.send(pack(STRUCT_BYTE, 0b1))
    
    rhead = DictionaryHeader()
    rhead.size = 59863
    rhead.operation = DictionaryHeader.ADD
    sendADDRequest(ssl_sock, rhead)
    response1 = readResponse(ssl_sock)
    print "ADD RESPONSE: ", response1, "\n"

    rhead2 = DictionaryHeader()
    rhead2.key = response1.key
    rhead2.operation = DictionaryHeader.GET
    sendGETRequest(ssl_sock, rhead2)
    response2 = readResponse(ssl_sock)
    print "GET RESPONSE: ", response2, "\n"
    
    rhead3 = DictionaryHeader()
    rhead3.key = response1.key
    rhead3.operation = DictionaryHeader.DELETE
    sendGETRequest(ssl_sock, rhead3)
    response3 = readResponse(ssl_sock)
    print "DELETE RESPONSE: ", response3, "\n"

    
    ssl_sock.close();
    print 'closed'
    
    
