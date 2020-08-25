#!/usr/bin/env python3.7

import http.server as http
import json

class APIServer(http.BaseHTTPRequestHandler):
	def __call__(self, *args):
		super().__init__(*args);
		return 0;

	def log_message(self, format, *args):
		return 0;

	def require_args(self, required, args):
		for i in required:
			try:
				args[i];
				args[i][0];
			except:
				return False;
		return True;

	def decode_json(self, data):
		return json.dumps(data, sort_keys=True, indent="\t", separators=(",", ": "), ensure_ascii=False);
