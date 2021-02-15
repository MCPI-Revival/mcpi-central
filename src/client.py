#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  client.py
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

class APIClient(APIBaseServer):
	def __init__(self, auth_server):
		self.__err = """{\n\t"error": "Not found."\n}""";
		self.token = None;
		self.stop = False;
		self.auth_server = auth_server or "https://mcpi-central.herokuapp.com";

	def get_token(self, code):
		res = requests.get(f"""{self.auth_server}/auth?code={code}""");
		res.raise_for_status();
		return res.json();

	def new_server(self, name, ip, port):
		if self.token is None:
			return -1;
		headers = {
			"Authorization": self.token
		};
		res = requests.get(f"""{self.auth_server}/servers/new?ip={ip}&port={port}&name={name}""", headers=headers);
		res.raise_for_status();
		return res.json();

	def update_server(self, name, ip, port):
		if self.token is None:
			return -1;
		headers = {
			"Authorization": self.token
		};
		print(self.token);
		res = requests.get(f"""{self.auth_server}/servers/update?ip={ip}&port={port}&name={name}""", headers=headers);
		res.raise_for_status();
		return res.json();

	def get_server(self, name):
		res = requests.get(f"""{self.auth_server}/server?name={name}""");
		res.raise_for_status();
		return res.json();

	def get_servers(self):
		res = requests.get(f"""{self.auth_server}/servers""");
		res.raise_for_status();
		return res.json();

	def login(self):
		server = http.HTTPServer(("0.0.0.0", 19140), self);
		server.timeout = 1;
		while not self.stop:
			server.handle_request();
		return 0;

	def do_GET(self):
		code = 200;
		query = parse_qs(urlparse(self.path).query);

		self.server_version = "MCPI-Central API";
		self.sys_version = "";

		if self.path[:11] == "/callback_auth?code=" and self.require_args(["code"], query):
			token = self.get_token(query["code"][0]);
			reply = "You can now close this window.";
			self.token = token["token"];
			self.stop = True;
		else:
			reply = self.__err;
			code = 404;

		self.send_response(code);
		self.send_header("Content-Type", "text/html");
		self.end_headers();

		self.wfile.write(reply.encode());
		self.wfile.write("\n".encode());
		return 0;
