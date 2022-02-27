#!/usr/bin/env python3
"""
Copyright 2022 Travis Conway

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
   this list of conditions and the following disclaimer in the documentation 
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
   may be used to endorse or promote products derived from this software without 
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.


  This script uses GeoIP2 to look up information regarding an IP or Hostname
  This assume a working DNS server and downloaded database.
  Set the DB path to the variable GeoIP2CityDBPath

  This script is really written to only work on my machine.
  Environemnt:
    macOS 12.1
    Python 3.9
    Homebrew
      geoipupdate (license required for database download)
    PIP3
      GeoIP2

  Use of this script may require modifications.
"""
import geoip2.database
import sys
import re
import socket

#Set these variables
GeoIP2CityDBPath="/opt/homebrew/var/GeoIP/GeoLite2-City.mmdb"


#Script Below
ip=None

myname=sys.argv[0].split('/')[-1]

try:
  input_ip=str(sys.argv[1]).strip()
except:
  print("Unable to determine input.")
  print("Usage:")
  print(myname + " [ip/host]")
  print("Example: " + myname + " 208.160.251.23")
  print("Example: " + myname + " google.com")
  exit(4)
  
regex="^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"

if re.search(":",input_ip):
  print("IPv6 not supported at this time")
  exit(3)

if re.search(regex,input_ip):
  ip = input_ip
else:
  print("Looking up IP for host: " + input_ip)
  try:
    ip = socket.gethostbyname(input_ip)
  except:
    print("Unable to look up IP. Quitting")
    exit(2)

if ip != None: 
  with geoip2.database.Reader(GeoIP2CityDBPath) as client:

    # You can also use `client.city` or `client.insights`
    # `client.insights` is not available to GeoLite2 users
    response = client.city(ip)

    print("IP: " + ip)
    print("City: " + str(response.city.name))
    print("Country: " + str(response.country.name))
    print("Registered Country: " + str(response.registered_country.name))
    print("Timezone: " + str(response.location.time_zone))
    print("Traits: ")
    print("\tASN: " + str(response.traits.autonomous_system_number) + " " + str(response.traits.autonomous_system_organization))
    print("\tNetwork: " + str(response.traits.network))
else:
  print("There is no ip address given. " + ip)
