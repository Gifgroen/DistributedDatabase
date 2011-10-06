"""
An entry in the dictionaryTable
"""
class LocationEntry(object):
	"""
	An entry is initialized with a key and a location where the data is stored
	"""
	def __init__(self, key, location):
	    self.offset = 0
	    self.length = 0
	    self.host = 0
	    self.port = 0
	    self.isWritten = False
	    self.location = str(location)

	def __repr__(self):
		return self.key, " -> ", self.location

	def getStorageHeader(self):
		pass
