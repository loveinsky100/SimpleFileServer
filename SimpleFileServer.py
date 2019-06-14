#!/usr/bin/python
# -*- coding: utf-8 -*-  

import socket
import SocketServer
import BaseHTTPServer
import cgi
import os, stat, sys
from SimpleHTTPServer import SimpleHTTPRequestHandler
import argparse
import urllib
import json

WORK_DIR = os.getcwd()
SERVERT_PORT = 8000

class PostHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     }
        )
        self.send_response(200)
        self.end_headers()
        self.wfile.write('success')
        path = WORK_DIR + str(self.path)
        path = urllib.unquote(path).decode('utf-8', 'replace')
        for field in form.keys():
            field_item = form[field]
            filename = urllib.unquote(field_item.filename).decode('utf-8', 'replace')
            if '/' != path:
              filename = '/' + filename
              pass
            filename = path + filename
            filevalue  = field_item.value
            if not os.path.exists(path):
              os.makedirs(path)
            with open(filename.decode('utf-8'),'wb') as f:
                f.write(filevalue)

            os.chmod(filename, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
        return

    def do_GET(self):
        path = WORK_DIR + str(self.path)
        path = urllib.unquote(path).decode('utf-8', 'replace')
        if os.path.isfile(path):
          # 下载此文件
          self.path = path
          f = self.send_file(path)
          if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()
        elif os.path.isdir(path):
          # 读取所有文件信息，然后返回json出去
          self.send_dir(path)
        else:
          self.send_response(404)
          self.end_headers()

    def send_file(self, path):
        f = None
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        try:
            self.send_response(200)
            self.send_header("Content-type", 'multipart/form-data')
            self.send_header("Content-Disposition", 'attachment;fileName=' + os.path.basename(path))
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def send_dir(self, path):
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None

        list.sort(key=lambda a: a.lower())
        fileAndDirMap = {}

        files = []
        dirs = []
        links = []
        fileAndDirMap["files"] = files
        fileAndDirMap["dirs"] = dirs
        fileAndDirMap["links"] = links
        
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                dirs.append(displayname)
            if os.path.islink(fullname):
                links.append(displayname)
            if os.path.isfile(fullname):
                files.append(displayname)
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(fileAndDirMap))

class ForkingHTTPServer(SocketServer.ForkingTCPServer):

   allow_reuse_address = 1

   def server_bind(self):
       """Override server_bind to store the server name."""
       SocketServer.TCPServer.server_bind(self)
       host, port = self.socket.getsockname()[:2]
       self.server_name = socket.getfqdn(host)
       self.server_port = port

def run(HandlerClass=PostHandler,
        ServerClass=ForkingHTTPServer,
        protocol="HTTP/1.0"):
    server_address = ('', SERVERT_PORT)

    HandlerClass.protocol_version = protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('-d', type=str, default = None)
    parser.add_argument('-p', type=str, default = 8000)
    args = parser.parse_args()
    work = args.d
    port = int(args.p)
    if work is not None:
      WORK_DIR = work
      pass

    SERVERT_PORT = port
    print("工作目录: " + WORK_DIR + " 服务端口: " + str(SERVERT_PORT))
    run()