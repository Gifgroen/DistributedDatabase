#!/usr/bin/env python
import sys, ssl, socket, time
from hashlib import sha1
from struct import pack

from communication_pb2 import HashedStorageHeader, StorageHeader

from storageserver import PRIVATE_HASH_KEY # for testing only

HOST = 'localhost'    # The remote host
PORT = 7777           # The same port as used by the server

STRUCT_BYTE = "!B"


if __name__ == '__main__':
    print 'Creating socket'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(s, ca_certs="sslcert/cert.pem", cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_SSLv23)
    print 'Connecting'
    ssl_sock.connect((HOST, PORT))
    
    # protocol version
    ssl_sock.send(pack(STRUCT_BYTE, 0b1))
    
    # construct message
    msg = HashedStorageHeader()
    msg.header.operation = StorageHeader.READ
    msg.header.offset = 0
    msg.header.length = 0
    msg.header.requestTimestamp = int(time.time())
    msg.hashAlgorithm = HashedStorageHeader.SHA1
    sha1hash = sha1(msg.header.SerializeToString() + PRIVATE_HASH_KEY)
    msg.hash = sha1hash.digest()
    
    print 'hash:', sha1hash.hexdigest() 
    
    msgData = msg.SerializeToString()
    assert len(msgData) < 256
    ssl_sock.send(pack(STRUCT_BYTE, len(msgData)))
    ssl_sock.send(msgData)
    
    ssl_sock.close();
    print 'closed'
    
    