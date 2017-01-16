#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  handler.py
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
import mimetypes
import os, traceback, sys
from .res import HTTPRes

class WebHandler(socketserver.BaseRequestHandler):
    def __init__ (self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()
    
    def parse_host (self, host):
        splt = host.split (".")
        
        if len(splt) == 1:
            if host == "localhost":
                return "www"
        elif len(splt) == 2:
            if host == self.server.config.domain:
                return "www"
            else:
                return splt[0]
        else:
            return splt[0]
    
    def gen_response (self, parsed):
        if (parsed["method"] != "GET"):
            return str("%s %s NOT IMPLEMENTED\n" % (parsed["version"], HTTPRes.IMPLEMENTED)).encode()
        if not mimetypes.inited:
            mimetypes.init()
        
        subroot = ""
        try:
            self.server.config.subdomains[self.parse_host(parsed["Host"])]
        except KeyError:
            subroot = self.server.config.root
        else:
            subroot = self.server.config.subdomains[self.parse_host(parsed["Host"])]
        
        if parsed["path"] == "/":
            parsed["path"] = "/index.html"
        
        fp = "%s%s" % (subroot, parsed["path"])
        if not os.path.isfile(fp):
            self.server.log ("%s: no such file or directory" % fp)
            return str("%s %s NOT FOUND\n" % (parsed["version"], HTTPRes.NOTFOUND)).encode()
        mtype = mimetypes.guess_type (fp)[0]
        if not mtype:
            mtype = "text/plain"
        read = open(fp, "rb").read()
        template = str("%s 200 OK\nContent-Type: %s\n\n" % (parsed["version"], mtype)).encode()
        template += read
        return template
    
    def parse_http (self, request):
        lines = str(request)[2:-1].split ("\\r\\n")
        ret = {}
        req_pars = lines[0].split (" ")
        if len (req_pars) != 3:
            self.server.log (request)
            return
        self.server.log (lines[0], "REQUEST")
        ret["method"] = req_pars[0]
        ret["path"] = req_pars[1]
        ret["version"] = req_pars[2]
        for line in lines[1:]: 
            parsed = line.split (": ")
            if len(parsed) != 2:
                ret["body"] = parsed[0]
            else:
                ret[parsed[0]] = parsed[1]
        return ret
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        try:
            parsed = self.parse_http(self.data)
            if (parsed == None):
                res = ("%s %s Bad Request\n" % ("HTTP/1.1", HTTPRes.BADREQ)).encode()
            else:
                res = self.gen_response (parsed)
        except:
            traceback.print_exc(file=sys.stdout)
            res = ("%s %s INTERNAL ERROR\n" % ("HTTP/1.1", HTTPRes.INTERN)).encode()
        try:
            self.server.log (res[0:str(res, 'utf-8').find("\n\n")], "RESPONSE")
        except UnicodeDecodeError:
            self.server.log ("Cant decode response (but it was send, image most likely)", "RESPONSE")
        self.request.sendall(res)
