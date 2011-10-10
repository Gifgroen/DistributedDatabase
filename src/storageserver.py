#!/usr/bin/env python

import sys
from optparse import OptionParser
from twisted.python import log

from generic.genericserver import FixedLengthMessageServer
from generic.protocol import BinaryMessageProtocol
from storage.handler import StorageRequestHandler
from storage.storagedb import StorageDatabase
from storage.xorpartnerconnection import XORPartnerConnection


class StorageServer(FixedLengthMessageServer):
    def __init__(self, options, args):
        super(StorageServer, self).__init__(options, args)
        self.factory.db = StorageDatabase(options.databasefile, options.databasesize)
        self.factory.db.start()
        self.factory.handlerClass = StorageRequestHandler
        self.factory.protocol = BinaryMessageProtocol
        self.factory.protocolVersion = 0b1
        if options.xor_host:
            log.msg("MODE: Public storage server")
            self.factory.xor_server_connection = XORPartnerConnection(options.xor_host, options.xor_port)
            self.factory.xor_server_connection.start()
        else:
            log.msg("MODE: Private XOR replication server")

if __name__ == '__main__':
    
    parser = OptionParser()
    StorageServer.addServerOptions(parser)
    
    parser.add_option("-d", "--db", dest="databasefile", default="storagedb.bin", help="loctation of database file", metavar="FILE")
    parser.add_option("-s", "--dbsize", dest="databasesize", default=100*1024*1024, help="size of database in bytes")
    
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
    parser.add_option("--xor_host", dest="xor_host", default=None, help="RAID4 XOR partner host")
    parser.add_option("--xor_port", dest="xor_port", default=8989, help="RAID4 XOR partner port")
    
    
    (options, args) = parser.parse_args()
    
    if options.verbose:
        log.startLogging(sys.stdout)
    
    server = StorageServer(options, args)    
    server.run()
