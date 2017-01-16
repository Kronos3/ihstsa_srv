#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  res.py
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


class HTTPRes:
    # 200 class (success)
    OK = 200
    
    # 300 class (redirection)
    REDIRPERM = 301 # Perminant redirect
    PROXY = 305 # Proxy required
    
    # 400 class (client errors)
    BADREQ = 400 # Bad request
    UNAUTH = 401 # Unauthorized
    FORBIDDEN = 403 # Forbidden (file permissions
    NOTFOUND = 404 # No such file or directory
    
    # 500 class (server errors)
    INTERN = 500 # Server error (caused by exceptions
    IMPLEMENTED = 501 # method not found
    BADGATE = 502 # Invalid response from another server
    UNAVAILIABLE = 503 # Method found but not working
    TIMEOUT = 504 # No response from another server
    HTTPVER = 505 # HTTP Version not 1.0 or 1.1
    NETAUTH = 511 # Need auth before continuing
