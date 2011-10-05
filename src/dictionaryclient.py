#!/usr/bin/env python
import sys, ssl, socket, time
from hashlib import sha1
from struct import pack, unpack

from generic.communication_pb2 import HashedStorageHeader, StorageHeader, DictionaryResponseHeader

from storage.handler import PRIVATE_HASH_KEY # for testing only

HOST = 'localhost'    # The remote host
PORT = 8989           # The same port as used by the server

STRUCT_BYTE = "!B"


def sign(msg):
    msg.header.requestTimestamp = int(time.time())
    msg.hashAlgorithm = HashedStorageHeader.SHA1
    sha1hash = sha1(msg.header.SerializeToString() + PRIVATE_HASH_KEY)
    msg.hash = sha1hash.digest()

    print 'hash:', sha1hash.hexdigest()


def readNBytes(ssl_sock, numBytes):
    print 'read %d bytes' % numBytes
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


def createRequestHeader(operation, offset, length):
    rhead = HashedStorageHeader()
    rhead.header.operation = operation
    rhead.header.offset = offset
    rhead.header.length = length
    sign(rhead)

    return rhead

def readResponse(ssl_sock):
    responseHeaderLength = unpack(STRUCT_BYTE, readNBytes(ssl_sock, 1))[0]
    responseHeaderData = readNBytes(ssl_sock, responseHeaderLength)
    print len(responseHeaderData)
    responseHeader = DictionaryResponseHeader()
    responseHeader.ParseFromString(responseHeaderData)

    return responseHeader

def sendADDRequest(ssl_sock, offset, data):
    # construct ADD message
    rhead = createRequestHeader(StorageHeader.WRITE, offset, len(data))
    sendMsg(ssl_sock, rhead)

def sendGETRequest(ssl_sock, offset, length):
    # construct GET message
    rhead = createRequestHeader(StorageHeader.READ, offset, length)
    sendMsg(ssl_sock, rhead)


def sendDELETERequest(ssl_sock, offset, length):
    # construct DELETE message
    pass # XOR HERE??


if __name__ == '__main__':
    print 'Creating socket \n'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(s, ca_certs="sslcert/cert.pem", cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_SSLv23)

    print 'Connecting \n'
    ssl_sock.connect((HOST, PORT))
    # protocol version
    ssl_sock.send(pack(STRUCT_BYTE, 0b1))    

    data = "EEN HELE LANGE STRING MET DATA DIE OVER EEN LIJNTJE GAAT> HOPEN DAT IE NIET TE LANG IS!!!!!!!!!!!111one"
    
    sendADDRequest(ssl_sock, 0, data)
    response1 = readResponse(ssl_sock)
    print "RESPONSE: ", response1, "\n"

    sendGETRequest(ssl_sock, 0, len(data))
    response2 = readResponse(ssl_sock)
    print "RESPONSE: ", response2
    
    ssl_sock.close();
    print 'closed'
    
    
