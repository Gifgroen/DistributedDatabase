"""
An entry in the dictionaryTable
"""
class TableEntry(object):
	"""
	An entry is initialized with a key and a location where the data is stored
	"""
	def __init__(self, key, location):
		self.key = key
		self.location = str(location)

	def __repr__(self):
		return self.key, " -> ", self.location
