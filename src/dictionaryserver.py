#!/usr/bin/env python

import sys
from optparse import OptionParser
from twisted.python import log

from generic.genericserver import FixedLengthMessageServer
from generic.protocol import BinaryMessageProtocol

from dictionary.handler import DictionaryRequestHandler
from dictionary.server import LocationHandler


class DictionaryServer(FixedLengthMessageServer):
    def __init__(self, options, args):
        super(DictionaryServer, self).__init__(options, args)
        self.factory.handlerClass = DictionaryRequestHandler
        self.factory.protocol = BinaryMessageProtocol
        self.factory.protocolVersion = 0b1
        self.factory.delegate = LocationHandler()

if __name__ == '__main__':
    
    parser = OptionParser()
    DictionaryServer.addServerOptions(parser)
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
    
    (options, args) = parser.parse_args()
    
    if options.verbose:
        log.startLogging(sys.stdout)
    
    server = DictionaryServer(options, args)    
    server.run()
