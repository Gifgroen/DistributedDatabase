#!/usr/bin/env python

from optparse import OptionParser
from generic.genericserver import ProtoMessageServer
from storage.headerparser import StorageHeaderParser
from storage.storagedb import StorageDatabase

class StorageServer(ProtoMessageServer):
    def __init__(self, options, args):
        super(StorageServer, self).__init__(options, args)
        self.db = StorageDatabase(options.databasefile)
        self.db.start()


if __name__ == '__main__':
    parser = OptionParser()
    ProtoMessageServer.addServerOptions(parser)
    parser.add_option("-d", "--db", dest="databasefile", default="storagedb.bin", help="loctation of database file", metavar="FILE")
    
    (options, args) = parser.parse_args()
    server = StorageServer(options, args)
    server.setHeaderParserClass(StorageHeaderParser)
    
    server.run()
