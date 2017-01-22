#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  server.py
#  
#  Copyright 2017 Andrei Tumbar <atuser@Kronos>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import socketserver
from . import handler
from . import config as cfg
import time
import os, sys, socket, ssl

class WebSite:
    def __init__ (self, fp):
        self.config = cfg.Config ()
        if not os.path.isfile(fp):
            raise FileNotFoundError("No such file: '%s'" % fp)
        self.config.read (fp)
        self.servers = {}
        for x in self.config.parse_server (os.path.realpath(fp)[0:os.path.realpath(fp).rfind('/')]):
            if x.ssl != False:
                self.servers[x.port] = WebServerSSL ((x.ip, x.port), handler.WebHandler, x.ssl)
            else:
                self.servers[x.port] = WebServer ((x.ip, x.port), handler.WebHandler)
            self.servers[x.port].configure (x)
            self.servers[x.port].log ("Will bind localhost to port %s" % x.port, "INFO")
    
    def start (self):
        for port in self.servers:
            if (os.fork ()):
                self.servers[port].log ("started server on port %s" % port, "INIT")
                self.servers[port].serve_forever ()
    
    def end (self):
        for port in self.servers:
            self.servers[port].log ("stopping (%s)" % port, "EXIT")
            self.server[port].logfile.close()
            self.servers[port].server_close()

class WebServer (socketserver.TCPServer):
    def __init__ (self, 
                  server_address, 
                  RequestHandlerClass,
                  bind_and_activate=True):
        self.has_ssl = False
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=False)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise

    
    def configure (self, cfg):
        self.config = cfg
        self.logfile = open ( self.config.log, "a+" ) # Truncate the file to speed the opening of the file
        self.logfile.truncate(0)
        if self.config.ssl:
            self.certfile = self.config.ssl["cert"]
            self.keyfile = self.config.ssl["key"]
    
    def log (self, message, _type="INFO"):
        msg = "[%s] %s\t%s\n" % (time.asctime( time.localtime(time.time()) ), _type, message)
        print (msg)
        sys.stdout.flush()
        self.logfile.write (msg)
        self.logfile.flush()

class WebServerSSL (WebServer):
    
    def __init__ (self, 
                  server_address, 
                  RequestHandlerClass,
                  _ssl,
                  bind_and_activate=True):
        self.has_ssl = True
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=False)
        _socket = socket.socket(self.address_family,
                                self.socket_type)
        
        self.socket = ssl.wrap_socket (_socket, certfile=_ssl["cert"], keyfile=_ssl["key"], server_side=True)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise
