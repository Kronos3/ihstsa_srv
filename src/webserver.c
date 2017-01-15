/*
 * webserver.c
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
#include <webserver.h>

struct Website * MAIN;

int read_config (struct WebServer**, char* filename); // Return the number of servers
void startServer (struct WebServer*, void (*handler) (struct mg_connection *nc, int ev, void *p)); // Fork this function to run multiple servers

void ev_handle (struct mg_connection *nc, int ev, void *p)
{
    // Get the Server instances by checking with the port
    struct WebServer * targ;
    uint16_t port_u16 = nc->sa.sin.sin_port;
    char port[6] = {0};
    sprintf (port, "%" PRIu16, port_u16);
    int i;
    for (i=0; i != MAIN->c; i++)
    {
        if ( strcmp ( port, MAIN->srvs[i]->port ) == 0 )
        {
            targ = MAIN->srvs[i];
            break;
        }
    }
    char* sub, dom, top;
    sscanf (p, "[^\n]\nHost: %[^.].%[^.].%[^\n]", sub, dom, top);
    char* root
}

void ev_handle_root (struct mg_connection *nc, int ev, void *p, char* root)
{
    if (ev == MG_EV_HTTP_REQUEST) {
        mg_serve_http(nc, (struct http_message *) p, s_http_server_opts);
    }
}
