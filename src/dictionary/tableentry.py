"""
An entry in the dictionaryTable
"""
class LocationEntry(object):
	"""
	An entry is initialized with a key and a location where the data is stored
	"""
	def __init__(self, key, location):
	    self.offset =
	    self.length =
	    self.host =
	    self.port =
	    self.isWritten = False
		self.location = str(location)

	def __repr__(self):
		return self.key, " -> ", self.location

    def getStorageHeader(self):
        pass
