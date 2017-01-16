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

class domain:
    has_subdomain = False
    subdomain = ""
    domain = ""
    is_local = False
    
    def __init__ (self, host):
        
        splt = host.split (".")
        l = len(splt)
        if "localhost" in host:
            self.is_local = True
            self.domain = "localhost"
        if l == 1 and self.is_local:
            self.has_subdomain = False # Dont redirect to www for localally hosted servers
        if l == 2 and not self.is_local:
            self.has_subdomain = False
            self.domain = host
        if l == 2 and self.is_local:
            self.subdomain = splt[0]
            self.has_subdomain = True
        if l == 3:
            self.has_subdomain = True
            self.subdomain = splt[0]
            self.domain = '.'.join ((splt[1], splt[2]))

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
    
    def gen_response (self, parsed):
        if (parsed["method"] != "GET"):
            return (("%s %s NOT IMPLEMENTED\n" % (parsed["version"], HTTPRes.IMPLEMENTED)).encode(), HTTPRes.IMPLEMENTED)
        if not mimetypes.inited:
            mimetypes.init()
        
        pdomain = domain(parsed["Host"])
        subroot = ""
        try:
            self.server.config.subdomains[pdomain.subdomain]
        except KeyError:
            subroot = self.server.config.root
        else:
            subroot = self.server.config.subdomains[pdomain.subdomain]
        
        if self.server.config.forcewww and not pdomain.has_subdomain:
            if (self.server.has_ssl):
                return (("%s %s Moved Permanently\nLocation: https://www.%s/\n\n" % (parsed["version"], HTTPRes.REDIRPERM, parsed["Host"])).encode(), HTTPRes.REDIRPERM) # Send to https
            else:
                return (("%s %s Moved Permanently\nLocation: http://www.%s/\n\n" % (parsed["version"], HTTPRes.REDIRPERM, parsed["Host"])).encode(), HTTPRes.REDIRPERM) # Send to http
        
        if self.server.config.redirect != "False":
            return (("%s %s Moved Permanently\nLocation: %s\n\n" % (parsed["version"], HTTPRes.REDIRPERM, self.server.config.redirect)).encode(), HTTPRes.REDIRPERM)
        
        if parsed["path"] == "/":
            parsed["path"] = "/index.html"
        
        fp = "%s%s" % (subroot, parsed["path"])
        if not os.path.isfile(fp):
            self.server.log ("%s: no such file or directory" % fp)
            return (("%s %s NOT FOUND\n" % (parsed["version"], HTTPRes.NOTFOUND)).encode(), HTTPRes.NOTFOUND)
        mtype = mimetypes.guess_type (fp)[0]
        if not mtype:
            mtype = "text/plain"
        read = open(fp, "rb").read()
        template = ("%s %s OK\nContent-Type: %s\n\n" % (parsed["version"], HTTPRes.OK, mtype)).encode()
        template += read
        return template, HTTPRes.OK
    
    def parse_http (self, request):
        lines = str(request)[2:-1].split ("\\r\\n")
        ret = {}
        req_pars = lines[0].split (" ")
        if len (req_pars) != 3:
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
        status = 0
        try:
            parsed = self.parse_http(self.data)
            if (parsed == None):
                res = ("%s %s Bad Request\n" % ("HTTP/1.1", HTTPRes.BADREQ)).encode()
                status = HTTPRes.BADREQ
            else:
                res, status = self.gen_response (parsed)
        except:
            traceback.print_exc(file=sys.stdout)
            res = ("%s %s INTERNAL ERROR\n" % ("HTTP/1.1", HTTPRes.INTERN)).encode()
            status = HTTPRes.INTERN
        try:
            if res != ("%s %s Bad Request\n" % ("HTTP/1.1", HTTPRes.BADREQ)).encode():
                self.server.log (status, "RESPONSE")
        except UnicodeDecodeError:
            self.server.log ("Cant decode response (but it was sent, image most likely)", "RESPONSE")
        self.request.sendall(res)
