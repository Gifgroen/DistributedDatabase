#!/usr/bin/env python

import sys
from optparse import OptionParser
from Queue import Queue, Empty

from twisted.python import log
from twisted.internet import reactor

from generic.genericserver import FixedLengthMessageServer
from generic.protocol import BinaryMessageProtocol

from dictionary.handler import DictionaryRequestHandler
from dictionary.server import LocationHandler
from dictionary.admin import DictionaryAdminServer
from dictionary.replicanotifier import ReplicaNotifier

class DictionaryServer(FixedLengthMessageServer):
    def __init__(self, options, args):
        super(DictionaryServer, self).__init__(options, args)
        self.factory.handlerClass = DictionaryRequestHandler
        self.factory.protocol = BinaryMessageProtocol
        self.factory.protocolVersion = 0b1
        self.factory.delegate = LocationHandler('localhost', 8000)# TODO: should be set automatically
        self.factory.master = {}
        self.factory.isMaster = False
        self.factory.replicaList = []
        self.factory.replicaNotifier = ReplicaNotifier()

if __name__ == '__main__':
    parser = OptionParser()
    DictionaryServer.addServerOptions(parser)

    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
    parser.add_option("-a", "--adminport", type="int", dest="admin_port", help="Port of admin server")
    
    (options, args) = parser.parse_args()
    
    if options.verbose:
        log.startLogging(sys.stdout)
    
    # The actual DictServer that does all the work
    server = DictionaryServer(options, args)
    server.listen()
    # The manager that receives messages from the dictionaryManager
    adminServer = DictionaryAdminServer(options, args, server)
    adminServer.listen()

    # Run all services
    reactor.run()
