#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  authserver.py
#
#  Copyright 2020 Alvarito050506 <donfrutosgomez@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 2 of the License.
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

import sys
import json
import http.server as http
import urllib.request
import requests
from os import environ
from urllib.parse import urlparse, parse_qs
from .base import *
import uuid


class AuthServer(APIBaseServer):
    def __init__(self, auth_server):
        self.__err = """{\n\t"error": "Not found."\n}""";
        self.token = None;
        self.stop = False;
        self.auth_server = auth_server or "https://mcpi-central.herokuapp.com";

    def get_token(self, code):
        res = requests.get(f"""{self.auth_server}/auth?code={code}""");
        res.raise_for_status();
        return res.json();


    def getToken(self):
        return self.token

    def do_GET(self):
        code = 200;
        query = parse_qs(urlparse(self.path).query);

        self.server_version = "MCPI-Central API";
        self.sys_version = "";

        if self.path[:11] == "/auth?code=" and self.require_args(["code"], query):
            token = self.get_token(query["code"][0]);
            reply = "You can now close this window.";
            self.token = token["token"];
            #self.stop = True;
            self.uuid = uuid.uuid4().hex
            # res = requests.get(f"""{self.auth_server}/registertoken?token={self.token}""");
            # res.raise_for_status()
        elif self.path == "/gettoken" and self.require_args(["uuid"], query):
            if query["uuid"][0] == uuid:
                reply = self.token
        else:
            reply = self.__err;
            code = 404;

        self.send_response(code);
        self.send_header("Content-Type", "text/html");
        self.end_headers();

        self.wfile.write(reply.encode());
        self.wfile.write("\n".encode());
        return 0;


def start_authserver():
    aS = AuthServer("https://mcpi-central.herokuapp.com/")
    server = http.HTTPServer(("0.0.0.0", int(environ.get("PORT")), aS))
    server.timeout = 1;
    while not aS.stop:
        server.handle_request();
    return 0;