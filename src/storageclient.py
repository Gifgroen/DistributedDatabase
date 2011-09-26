#!/usr/bin/env python
import sys, ssl, socket, time
from hashlib import sha1
from struct import pack, unpack

from generic.communication_pb2 import HashedStorageHeader, StorageHeader, StorageResponseHeader

from storage.headerparser import PRIVATE_HASH_KEY # for testing only

HOST = 'localhost'    # The remote host
PORT = 8989           # The same port as used by the server

STRUCT_BYTE = "!B"


def sign(msg):
    msg.header.requestTimestamp = int(time.time())
    msg.hashAlgorithm = HashedStorageHeader.SHA1
    sha1hash = sha1(msg.header.SerializeToString() + PRIVATE_HASH_KEY)
    msg.hash = sha1hash.digest()
    
    print 'hash:', sha1hash.hexdigest()
    
def sendMsg(ssl_sock, msg):
    msgData = msg.SerializeToString()
    assert len(msgData) < 256
    ssl_sock.send(pack(STRUCT_BYTE, len(msgData)))
    ssl_sock.send(msgData)

def sendWriteRequest(ssl_sock, offset, data):
    # construct message
    msg = HashedStorageHeader()
    msg.header.operation = StorageHeader.WRITE
    msg.header.offset = offset
    msg.header.length = len(data)
    sign(msg)
    
    sendMsg(ssl_sock, msg)
    
    ssl_sock.send(data)

def sendReadRequest(ssl_sock, offset, length):
    msg = HashedStorageHeader()
    msg.header.operation = StorageHeader.READ
    msg.header.offset = offset
    msg.header.length = length
    sign(msg)
    sendMsg(ssl_sock, msg)
    

def readNBytes(ssl_sock, numBytes):
    print 'read %d bytes' % numBytes
    msgData = ''
    while len(msgData) != numBytes:
        restLength = numBytes - len(msgData)
        received = ssl_sock.read(restLength)
        msgData = msgData + received
    return msgData

def readResponse(ssl_sock):
    responseHeaderLength = unpack(STRUCT_BYTE, readNBytes(ssl_sock, 1))[0]
    responseHeaderData = readNBytes(ssl_sock, responseHeaderLength)
    print len(responseHeaderData)
    responseHeader = StorageResponseHeader()
    responseHeader.ParseFromString(responseHeaderData)
    if responseHeader.header.operation == StorageHeader.READ:
        print 'Read data:', readNBytes(ssl_sock, responseHeader.header.length)
    else: # written
        print 'Data written'
    

if __name__ == '__main__':
    print 'Creating socket'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(s, ca_certs="sslcert/cert.pem", cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_SSLv23)
    print 'Connecting'
    ssl_sock.connect((HOST, PORT))
    
    # protocol version
    ssl_sock.send(pack(STRUCT_BYTE, 0b1))
    
    data = "HELLO WORLD!!!!!"
    
    sendWriteRequest(ssl_sock, 0, data)
    readResponse(ssl_sock)
    
    sendReadRequest(ssl_sock, 0, len(data))
    readResponse(ssl_sock)
    
    ssl_sock.close();
    print 'closed'
    
    