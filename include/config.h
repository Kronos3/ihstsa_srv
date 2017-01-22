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

struct ssl_map {
    char* cert; // The fullchain certificate
    char* key; // The server private key
};

struct ServerConfig
{
    char* domain;
    char* log;
    char* root;
    char** subdomains;
    char** subdomain_mapped;
    ssl_map ssl;
    int has_ssl;
    int redirect;
    char* redir_site;
    int forcewww;
    char* ip;
    
};

struct ServerConfig * read_config (char* fname);
