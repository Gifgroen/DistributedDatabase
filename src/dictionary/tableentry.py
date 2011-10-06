from generic.communication_pb2 import DataLocation, StorageHeader
from storageclient import sign
from storage.handler import copyHeaderData

"""
An entry in the dictionaryTable
"""
class LocationEntry(object):
	"""
	An entry is initialized with a key and a location where the data is stored
	"""
	def __init__(self, host, port, offset, length):
	    self.isWritten = False

	    self.dataLocation = DataLocation()
	    self.dataLocation.host = host
	    self.dataLocation.port = port

	    self.dataLocation.header.header.offset = offset
	    self.dataLocation.header.header.length = length

	def __repr__(self):
	    return '%s %s' % (self.dataLocation, self.isWritten)

	def toWriteMessage(self):
	    self.dataLocation.header.header.operation = StorageHeader.WRITE
	    return self._toDataLocationMessage()
	    
	def toReadMessage(self):
	    self.dataLocation.header.header.operation = StorageHeader.READ
	    return self._toDataLocationMessage()

	def _toDataLocationMessage(self):
	    sign(self.dataLocation.header)
	    return self.dataLocation
