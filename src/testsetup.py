#!/usr/bin/env python

from subprocess import Popen
from time import sleep

if __name__ == '__main__':
    xor_host = "localhost"
    xor_port = "8080"
    
    xor_server = Popen(["./storageserver.py", "-p", xor_port, "-d", "db-xor.bin"])
    
    sleep(1) # ugly way to ensure that xor server is started
    
    server1 = Popen(["./storageserver.py", "-p", "8081", "-d", "db-1.bin", "--xor_host", xor_host, "--xor_port", xor_port])
    server2 = Popen(["./storageserver.py", "-p", "8082", "-d", "db-2.bin", "--xor_host", xor_host, "--xor_port", xor_port])
    
    try:
        xor_server.wait()
        server1.wait()
        server2.wait()
    except KeyboardInterrupt:# necessary?
        server2.terminate()
        server1.terminate()
        xor_server.terminate()