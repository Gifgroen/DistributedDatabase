from tableentry import TableEntry

"""
The distributed filetable of a Dictionary server that maps keys to locations
"""
class DictionaryTable(object):
	"""
	Create a location table that maps DB keys to a physical location
	"""
	def __init__(self):
		self.locationDict = {}

	"""
	Add an entry in the DictionaryTable
		@return: the reference location under which the data is stored
	"""
	def add(self, sizeOfData):
		print "ADD"

	"""
	Get a location from the locationDict
		@return: the location of the StorageServer that has the requested data
	"""
	def get(self, key):
		print "GET"
	
	"""
	Delete an entry (or key) from the location table. 
	The deletion of this key -> location pair throws away the pointer to the key.
		@return an acknowledgement message (OK, FAIL, ...)
	"""
	def delete(self, key):
		print "DELETE"
