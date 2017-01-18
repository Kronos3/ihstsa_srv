/*
 * config.h
 * 
 * Copyright 2017 Andrei Tumbar <atuser@Kronos>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */


#include <iostream>
#include <map>

using namespace std;

typedef struct {
    char* cert; // The fullchain certificate
    char* key; // The server private key
}ssl_map;

class ServerConfig:
    
    public:
    char* domain;
    char* log;
    char* root;
    map <char*, char*> subdomains;
    map <char*, ssl_map> ssl;
    char* redirect;
    bool forcewww;
    char* ip;
    
    ServerConfig (char* fname) {
        
    }
