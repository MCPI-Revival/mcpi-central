#
#  Makefile
#  
#  Copyright 2020 Alvarito050506 <donfrutosgomez@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; version 3 of the License.
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

pack:
	mkdir -p ./deb/
	mkdir -p ./deb/usr/lib/python3/dist-packages/mcpicentral
	mkdir -p ./deb/DEBIAN/
	cp -a ./src/. ./deb/usr/lib/python3/dist-packages/mcpicentral
	@echo "Package: mcpi-central" > ./deb/DEBIAN/control
	@echo "Version: 0.2.1" >> ./deb/DEBIAN/control
	@echo "Priority: optional" >> ./deb/DEBIAN/control
	@echo "Architecture: armhf" >> ./deb/DEBIAN/control
	@echo "Depends: python3" >> ./deb/DEBIAN/control
	@echo "Maintainer: Alvarito050506 <donfrutosgomez@gmail.com>" >> ./deb/DEBIAN/control
	@echo "Homepage: https://mcpi.tk" >> ./deb/DEBIAN/control
	@echo "Vcs-Browser: https://github.com/MCPI-Devs/mcpi-central" >> ./deb/DEBIAN/control
	@echo "Vcs-Git: https://github.com/MCPI-Devs/mcpi-central.git" >> ./deb/DEBIAN/control
	@echo "Description: MCPI centralized API.\n" >> ./deb/DEBIAN/control
	dpkg-deb -b ./deb/ ./mcpi-central_0.2.1-1.deb

clean:
	rm -rf ./deb/
	rm -f ./mcpi-central_*-*.deb
