#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  db.py
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

import psycopg2
import psycopg2.extras
from os import environ

class DBData:
	def __init__(self, url):
		self.conn = psycopg2.connect(url, sslmode="require");
		self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor);

	def setup(self):
		self.cur.execute("CREATE TABLE IF NOT EXISTS servers (name VARCHAR(64) NOT NULL, ip TEXT NOT NULL, port SMALLINT NOT NULL CHECK (port > 0), owner VARCHAR(64) NOT NULL, PRIMARY KEY (name));");
		self.cur.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(64) NOT NULL, email VARCHAR(64) NOT NULL, admin BOOLEAN DEFAULT 0, PRIMARY KEY (username));")
		self.conn.commit();
		return 0;

	def add_server(self, name, ip, port, owner):
		if not (len(name) < 64 and len(owner) < 64 and 0 < port < 32767):
			return -1;
		self.cur.execute("INSERT INTO servers (name, ip, port, owner) VALUES (%s, %s, %s, %s);", (name, ip, port, owner));
		self.conn.commit();
		return 0;

	def update_server(self, name, ip, port):
		if not (0 < port < 32767):
			return -1;
		self.cur.execute("UPDATE servers SET ip=%s, port=%s WHERE name=%s;", (ip, port, name));
		self.conn.commit();
		return 0;

	def get_server(self, name):
		self.cur.execute("SELECT * FROM servers WHERE name = %s;", (name,));
		return self.cur.fetchone();

	def get_servers(self):
		self.cur.execute("SELECT name FROM servers LIMIT 50;");
		return self.cur.fetchall();

	def register_user(self, username, email, admin):
		self.cur.execute("INSERT INTO users (username, email, admin) VALUES (%s, %s, %s);", (username, email, admin))
		self.conn.commit()
		return 0

	def get_user(self, email):
		self.cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
		return self.cur.fetchone()

	def check_admin(self, email):
		self.cur.execute("SELECT admin FROM users WHERE email = %s;", (email,))
		return self.cur.fetchone()

	def close(self):
		self.cur.close();
		self.conn.close();
		return 0;
