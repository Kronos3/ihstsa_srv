#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config.py
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

import configparser

class Server:
    domain = ""
    log = ""
    root = ""
    subdomains = {}
    port = None
    ssl = False
    redirect = False
    
    def __init__ (self):
        pass


class Config(configparser.ConfigParser):
    def parse_server (self):
        for s_server in self.sections ():
            server = Server ()
            server.domain = self[s_server]["domain"]
            server.log = self[s_server]["log"]
            server.root = self[s_server]["root"]
            exec ("server.subdomains = %s" % self[s_server]["subdomains"])
            server.port = int(s_server)
            exec ("server.ssl = %s" % self[s_server]["ssl"])
            print (server.ssl)
            server.redirect = self[s_server]["redirect"]
            server.forcewww = self[s_server]["forcewww"]
            yield server
