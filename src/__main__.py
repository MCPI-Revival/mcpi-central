#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  __main__.py
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

from mcpicentral import *
# import authserver
# from mcpicentral import src.authserver
#from mcpicentral import authserver

if __name__ == '__main__':

	#sys.exit(server.mcpi_central_server(environ.get("CLIENT_ID"), environ.get("CLIENT_SECRET"), environ.get("AUTH_CLIENT"), environ.get("DATABASE_URL")));
    sys.exit(authserver.start_authserver())