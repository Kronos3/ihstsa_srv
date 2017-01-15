/*
 * webserver.h
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


#include <stdio.h>
#include <stdlib.h>
#include <libconfig.h>
#include <mongoose.h>

typedef enum { false, true } bool;

struct subdomain {
    char* name;
    char* root;
};

struct ssl {
    char* cert;
    char* key;
}

struct WebServer {
    char* title;
    char* log;
    char* port;
    char* root;
    struct subdomain ** subdomains;
    int subc; // Subdomain count
    bool  use_ssl;
    struct ssl * _ssl;
};

struct Website {
    struct WebServer ** srvs;
    int c; // Count of servers
}

extern Website * MAIN;

int read_config (struct Website*, char* filename); // Return the number of servers
void startServer (struct WebServer*, void (*handler) (struct mg_connection *nc, int ev, void *p)); // Fork this function to run multiple servers
void ev_handle (struct mg_connection *nc, int ev, void *p);
void ev_handle_root (struct mg_connection *nc, int ev, void *p, char* root);
