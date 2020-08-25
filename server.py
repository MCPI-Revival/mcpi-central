#!/usr/bin/env python3.7

import sys
import json
import http.server as http
import urllib.request
import requests
from os import environ
from urllib.parse import urlparse, parse_qs
from db import *
from base import *

class APIHandler(APIServer):
	def __init__(self):
		self.__err = """{\n\t"error": "Not found."\n}""";
		self.db = DBData();
		self.db.setup();
		self.paths = {
			"/auth": ["code"],
			"/servers/new": ["token", "name", "ip", "port"],
			"/user": ["token"],
			"/server": ["name"],
			"/servers": [],
			"/servers/update": ["token", "name", "ip", "port"]
		};

	def get_token(self, code):
		data = {
			"client_id": environ.get("CLIENT_ID"),
			"client_secret": environ.get("CLIENT_SECRET"),
			"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": environ.get("AUTH_CLIENT"),
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

		self.server_version = "MCPI API";
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
			if url.path == "/auth":
				reply = self.decode_json({
					"token": self.get_token(query["code"][0])["access_token"]
				});
			elif url.path == "/user":
				reply = self.decode_json(self.get_user(query["token"][0]));
			elif url.path == "/servers/new":
				user = self.get_user(query["token"][0])["id"];
				self.db.add_server(query["name"][0], query["ip"][0], int(query["port"][0]), user);
				reply = self.decode_json({
					"name": query["name"][0],
					"ip": query["ip"][0],
					"port": int(query["port"][0]),
					"owner": user
				});
			elif url.path == "/servers/update":
				user = self.get_user(query["token"][0])["id"];
				if self.db.get_server(query["name"][0])["owner"] == user:
					self.db.update_server(query["name"][0], query["ip"][0], int(query["port"][0]));
					reply = self.decode_json({
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
				if servers is not None:
					reply = self.decode_json({
						"servers": servers
					});
			elif url.path == "/server":
				server = self.db.get_server(query["name"][0]);
				if server is not None:
					reply = self.decode_json(server);
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

def mcpi_api_server():
	handler = APIHandler();
	server = http.HTTPServer(("0.0.0.0", int(environ.get("PORT"))), handler);
	try:
		server.serve_forever();
	except KeyboardInterrupt:
		handler.db.close();
		print();
		return 0;

if __name__ == '__main__':
	sys.exit(mcpi_api_server());
