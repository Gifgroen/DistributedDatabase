from tableentry import LocationEntry

import freelist.memtable as memtable

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
        loc = memtable.getFreeSpace(sizeOfData)
        self.locationDict[loc["key"]] = LocationEntry(loc["hostname"], loc["port"], loc["offset"], loc["length"])

        # TODO return location
        return loc['key']

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
        if key not in self.locationDict:
            return False

        # get the location to free in freelist
        loc = self.locationDict[key]
        # Release in freelist
        memtable.releaseSpace(loc)
        del(loc)
        return True

            
        

        
        # TODO: Create Notification message and notify freelist
        
