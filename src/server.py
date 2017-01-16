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
from time import gmtime, strftime
import os, sys

class WebSite:
    def __init__ (self, fp):
        self.config = cfg.Config ()
        if not os.path.isfile(fp):
            raise FileNotFoundError("No such file: '%s'" % fp)
        self.config.read (fp)
        self.servers = {}
        for x in self.config.parse_server ():
            self.servers[x.port] = WebServer (("localhost", x.port), handler.WebHandler)
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
            self.servers[port].server_close()

class WebServer (socketserver.TCPServer):
    def configure (self, cfg):
        self.config = cfg
    
    def log (self, message, _type="INFO"):
        msg = "[%s] %s\t%s" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), _type, message)
        print (msg)
        sys.stdout.flush()
        os.system ("echo '%s' >> %s" % (msg, self.config.log))
