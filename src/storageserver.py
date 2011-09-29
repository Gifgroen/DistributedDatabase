#!/usr/bin/env python

import sys
from optparse import OptionParser
from twisted.python import log

from generic.genericserver import FixedLengthMessageServer
from generic.protocol import BinaryMessageProtocol
from storage.handler import StorageRequestHandler
from storage.storagedb import StorageDatabase


class StorageServer(FixedLengthMessageServer):
    def __init__(self, options, args):
        super(StorageServer, self).__init__(options, args)
        self.factory.db = StorageDatabase(options.databasefile)
        self.factory.db.start()
        self.factory.handlerClass = StorageRequestHandler
        self.factory.protocol = BinaryMessageProtocol
        self.factory.protocolVersion = 0b1

if __name__ == '__main__':
    
    parser = OptionParser()
    StorageServer.addServerOptions(parser)
    parser.add_option("-d", "--db", dest="databasefile", default="storagedb.bin", help="loctation of database file", metavar="FILE")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
    
    (options, args) = parser.parse_args()
    
    if options.verbose:
        log.startLogging(sys.stdout)
    
    server = StorageServer(options, args)    
    server.run()
