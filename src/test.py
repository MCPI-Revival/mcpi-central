#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test.py
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
from mcpicentral import *

def main():
	"""
	Creates a client instance, using the default server (https://mcpi-devs.herokuapp.com) and starts the log-in server.
	Go to https://discord.com/oauth2/authorize?client_id=744320103566540912&redirect_uri=http%3A%2F%2Flocalhost%3A19140%2Fauth&response_type=code&scope=identify%20email to log-in.
	"""
	client = APIClient(None);
	client.login();

	"""
	Prints the names of the first 50 servers in the database, as JSON, to `stdout`.
	"""
	print(client.get_servers());
	return 0;

if __name__ == '__main__':
	sys.exit(main());
