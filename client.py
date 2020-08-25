#!/usr/bin/env python3.7

import sys
import json
import http.server as http
import urllib.request
import requests
from os import environ
from urllib.parse import urlparse, parse_qs
from base import *

class APIClient(APIServer):
	def __init__(self):
		self.__err = """{\n\t"error": "Not found."\n}""";
		self.token = None;
		self.stop = False;
		self.server = environ.get("AUTH_SERVER") or "https://mcpi-devs.herokuapp.com";

	def get_token(self, code):
		res = requests.get(f"""{self.server}/auth?code={code}""");
		res.raise_for_status();
		return res.json();

	def new_server(self, name, ip, port):
		if self.token is None:
			return -1;
		res = requests.get(f"""{self.server}/servers/new?token={self.token}&ip={ip}&port={port}&name={name}""");
		res.raise_for_status();
		return res.json();

	def get_server(self, name):
		res = requests.get(f"""{self.server}/server?name={name}""");
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

		self.server_version = "MCPI API";
		self.sys_version = "";

		if self.path[:11] == "/auth?code=" and self.require_args(["code"], query):
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

def main():
	client = APIClient();
	client.login();
	print(client.get_server("StevePi"));
	return 0;

if __name__ == '__main__':
	sys.exit(main());
