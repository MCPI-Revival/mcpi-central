#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  server.py
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
from .db import *
from .base import *

class APIServer(APIBaseServer):
	def __init__(self, id, secret, client, db_url):
		self.__err = """{\n\t"error": "Not found."\n}""";
		self.db = DBData(db_url);
		self.db.setup();
		self.paths = {
			"/auth": ["code"],
			"/servers/new": ["token", "name", "ip", "port"],
			"/user": ["token"],
			"/server": ["name"],
			"/servers": [],
			"/servers/update": ["token", "name", "ip", "port"]
		};
		self.id = id;
		self.secret = secret;
		self.client = client;

	def get_token(self, code):
		data = {
			"client_id": self.id,
			"client_secret": self.secret,
			"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": self.client,
			"scope": "identify email"
		};
		headers = {
			"Content-Type": "application/x-www-form-urlencoded"
		};
		res = requests.post("https://discord.com/api/v6/oauth2/token", data=data, headers=headers);
		res.raise_for_status();
		return res.json();

	def get_user(self, token):
		headers = {
			"Authorization": f"Bearer {token}"
		};
		res = requests.get("https://discord.com/api/v6/users/@me", headers=headers);
		res.raise_for_status();
		return res.json();

	def do_GET(self):
		code = 200;
		reply = None;
		url = urlparse(self.path);
		query = parse_qs(url.query);

		self.server_version = "MCPI-Central API";
		self.sys_version = "";


		try:
			self.paths[url.path];
		except:
			reply = self.__err;
			code = 404;
			self.send_response(code);
			self.send_header("Content-Type", "application/json");
			self.end_headers();

			self.wfile.write(reply.encode());
			self.wfile.write("\n".encode());
			return 0;

		if self.require_args(self.paths[url.path], query):
			token = self.headers.get("Authorization");

			if url.path == "/auth":
				reply = self.encode_json({
					"token": self.get_token(query["code"][0])["access_token"]
				});
			elif url.path == "/user":
				reply = self.encode_json(self.get_user(token));
			elif url.path == "/servers/new":
				user = self.get_user(token)["id"];
				self.db.add_server(query["name"][0], query["ip"][0], int(query["port"][0]), user);
				reply = self.encode_json({
					"name": query["name"][0],
					"ip": query["ip"][0],
					"port": int(query["port"][0]),
					"owner": user
				});
			elif url.path == "/servers/update":
				user = self.get_user(token)["id"];
				if self.db.get_server(query["name"][0])["owner"] == user:
					self.db.update_server(query["name"][0], query["ip"][0], int(query["port"][0]));
					reply = self.encode_json({
						"name": query["name"][0],
						"ip": query["ip"][0],
						"port": int(query["port"][0]),
						"owner": user
					});
				else:
					code = 404;
					reply = self.__err;
			elif url.path == "/servers":
				servers = self.db.get_servers();
				server_arr = list();
				if servers is not None:
					for server in servers:
						server_arr.append(server["name"]);
					reply = self.encode_json({
						"servers": server_arr
					});
				else:
					code = 404;
					reply = self.__err;
			elif url.path == "/server":
				server = self.db.get_server(query["name"][0]);
				if server is not None:
					reply = self.encode_json(server);
				else:
					code = 404;
					reply = self.__err;
		else:
			reply = self.__err;
			code = 404;

		self.send_response(code);
		self.send_header("Content-Type", "application/json");
		self.end_headers();

		self.wfile.write(reply.encode());
		self.wfile.write("\n".encode());
		return 0;

def mcpi_central_server(id, secret, client, db_url):
	handler = APIServer(id, secret, client, db_url);
	server = http.HTTPServer(("0.0.0.0", int(environ.get("PORT"))), handler);
	try:
		server.serve_forever();
	except KeyboardInterrupt:
		handler.db.close();
		print();
		return 0;
