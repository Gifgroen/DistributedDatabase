#!/usr/bin/env python

from optparse import OptionParser
from generic.genericserver import ProtoMessageServer
from storage.headerparser import StorageHeaderParser


if __name__ == '__main__':
    parser = OptionParser()
    ProtoMessageServer.addServerOptions(parser)
    (options, args) = parser.parse_args()
    server = ProtoMessageServer(options, args)
    server.setHeaderParserClass(StorageHeaderParser)
    server.run()