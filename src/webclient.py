#!/usr/bin/env python

import cgi
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Storage webclient</title>
</head>

<body>
    <div>
        <h1>File upload</h1>
        <div>%s</div>
        <form enctype="multipart/form-data" action="/" method="post">
            <label for="file">File:</label>
            <input type="file" name="file" id="file"/> 
            <input type="submit" value="Upload" />
        </form>
    </div>
</body>

</html>
"""

class MyHandler(BaseHTTPRequestHandler):
    
    def _sendIndexPage(self, uploadedKey=""):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(PAGE % (uploadedKey))

    def do_GET(self):
        if self.path == '/':
            self._sendIndexPage()
        else:
            self.send_error(404, 'Page Not Found: %s' % self.path)
            
    def _handleFileUpload(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        print ctype
        assert ctype == 'multipart/form-data'
        query = cgi.parse_multipart(self.rfile, pdict)
        
        upfilecontent = query.get('upfile')
        self._sendIndexPage("Uploaded file to: %s" % upfilecontent[0])
        
        
    def do_POST(self):
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

