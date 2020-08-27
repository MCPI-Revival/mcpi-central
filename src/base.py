#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  base.py
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

import http.server as http
import json

class APIBaseServer(http.BaseHTTPRequestHandler):
	def __call__(self, *args):
		super().__init__(*args);
		return 0;

	def log_message(self, format, *args):
		return 0;

	def require_args(self, required, args):
		for i in required:
			try:
				if i != "token":
					args[i];
					args[i][0];
				elif i == "token" and self.headers.get("Authorization") is None:
					raise NameError;
			except:
				return False;
		return True;

	def encode_json(self, data):
		return json.dumps(data, sort_keys=True, indent="\t", separators=(",", ": "), ensure_ascii=False);
