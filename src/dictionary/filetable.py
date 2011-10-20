from tableentry import LocationEntry

import freelist.spacetable as spacetable

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
    def add(self, key, hostname, port, offset, length):
        if key not in self.locationDict:
            self.locationDict[key] = []
        self.locationDict[key].append(LocationEntry(hostname, port, offset, length))
            

    """
    Get a location from the locationDict
	@return: the location of the StorageServer that has the requested data
    """
    def get(self, key):
        if key in self.locationDict:
            return self.locationDict[key]
        return []
    
    """
    Delete an entry (or key) from the location table. 
    The deletion of this key -> location pair throws away the pointer to the key.
	@return an acknowledgement message (OK, FAIL, ...)
    """
    def delete(self, key):
        if key in self.locationDict:
            del self.locationDict[key]
            return True
        return False

        
