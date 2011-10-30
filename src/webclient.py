#!/usr/bin/env python

import cgi

from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


from client import store, retrieve

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Storage webclient</title>
</head>

<body>
    <div>
        <p><a href="/">Back to home</a></p>
        <h1>File upload</h1>
        <div>%s</div>
        <form enctype="multipart/form-data" action="/" method="post">
            <p>
                <label for="file">File:</label>
                <input id="file" type="file" name="file">
            </p>
            <p>
                <input type="submit" value="Upload">
            </p>
        </form>
    </div>
</body>

</html>
"""

class MyHandler(BaseHTTPRequestHandler):
    
    def _sendIndexPage(self, msg=""):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(PAGE % (msg))

    def _sendData(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(data)

    def _handleGet(self, key):
        data = retrieve(key)
        if data:
            self._sendData(data)
        else:
            self._sendIndexPage('File Not Found: %s' % key)

    def do_GET(self):
        if self.path == '/':
            self._sendIndexPage()
        else:
            self._handleGet(self.path[1:-1])
            
    def _handleFileUpload(self):
        if 'file' not in self.postvars:
            self._sendIndexPage("Nothing uploaded")
        else:
            fileContent = self.postvars['file'][0]
            try:
                key = store(fileContent)
                self._sendIndexPage('File stored with key: <a href="/%s/">%s</a>' % (key, key))
            except:
                self._sendIndexPage("Error during file upload, try again...")
        
        
    def do_POST(self):
        # parse post vars
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            self.postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            self.postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            self.postvars = {}
        # select handler for path
        if self.path == '/':
            self._handleFileUpload()
        else:
            self.send_error(404, 'Page Not Found: %s' % self.path)
        

def main():
    global INDEX_PAGE
    try:
        server = HTTPServer(('', 7777), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

