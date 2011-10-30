from threading import Thread, currentThread
from time import time, sleep

from freelistclient import SimpleFreelistTestClient
from dictionarymanager import DictionaryAdminClient

from storagemanager import checkAllStorageServers
from storagemanager import stop as storageStop
from storagemanager import addServer as addStorageServer
from storagemanager import setDictionaryConnection, setFreelistConnection
from storagemanager import startNewGroup as startNewStorageGroup


HEARTBEAT_SECONDS = 10 # low for testing
HEARTBEAT_THREAD = None


def heartBeatJob():
    global HEARTBEAT_THREAD
    while HEARTBEAT_THREAD == currentThread():
        start = time()
        
        checkAllStorageServers()
        
        # check again in heartbeat time seconds (minus the time the job took)
        sleep_secs = max(HEARTBEAT_SECONDS - (int(time() - start)), 0)
        #print 'sleep %d seconds' % sleep_secs
        sleep(sleep_secs)
    print 'heartbeat thread stopped'
    
    
def stop():
    # stop heartbeat
    global HEARTBEAT_THREAD
    HEARTBEAT_THREAD = None
    
    storageStop()
    
    
def start():
    global HEARTBEAT_THREAD
    assert HEARTBEAT_THREAD is None
    HEARTBEAT_THREAD = Thread(target=heartBeatJob, name='HeartBeatJob')
    HEARTBEAT_THREAD.start()

def testSetup():
    setFreelistConnection(SimpleFreelistTestClient('localhost', 8000))
    setDictionaryConnection(DictionaryAdminClient('localhost', 8001))
    
    addStorageServer('localhost', 8080, 8081)
    addStorageServer('localhost', 8082, 8083)
    addStorageServer('localhost', 8084, 8085)
    addStorageServer('localhost', 8086, 8087)
    
    startNewStorageGroup()
    
    
        