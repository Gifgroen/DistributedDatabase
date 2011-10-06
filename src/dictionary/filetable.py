from tableentry import LocationEntry

"""
The distributed filetable of a Dictionary server that maps keys to locations
"""
class DictionaryTable(object):
    """
    Create a location table that maps DB keys to a physical location
    """
    def __init__(self):
        # key -> [tableentrie]
        self.locationDict = {}

    """
    Add an entry in the DictionaryTable
	@return: the reference location under which the data is stored
    """
    def add(self, sizeOfData):
        # get space from freelist
        key = "randKey"
        self.locationDict[key] = LocationEntry("localhost", 4242, 0, sizeOfData)

        # TODO return location
        return key

    """
    Get a location from the locationDict
	@return: the location of the StorageServer that has the requested data
    """
    def get(self, key):
        print 'get', key, self.locationDict
        if key in self.locationDict:
            return [self.locationDict[key]]
        return None
    
    """
    Delete an entry (or key) from the location table. 
    The deletion of this key -> location pair throws away the pointer to the key.
	@return an acknowledgement message (OK, FAIL, ...)
    """
    def delete(self, key):
        # TODO: Create Notification message and notify freelist
        if key in self.locationDict:
            self.locationDict.remove(key)
