#!/usr/bin/env python
# Copyright 2012 Rackspace

# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""challenge1.py.
Build a number of servers and display the networking information, root 
password and server name for each server built.

Usage:
challenge1.py
challenge1.py (-h | --help)

Options:
-h --help    Show this help screen

"""

import pyrax
import time
import sys
import os
from docopt import docopt

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)

cs = pyrax.cloudservers

def main():
  i = 1
  print
  pre = str(raw_input ("What would you like your servers to be named? "))
  print
  servercount = int(raw_input ("How many servers would you like to create? "))
  while i <= servercount:
    servname = pre + str(i)
    create(servname)
    i += 1
  print
  print "Done!"
  print

def create(servname):
  image = "da1f0392-8c64-468f-a839-a9e56caebf07"
  server = cs.servers.create(servname, image, "2")
  root = server.adminPass
  print
  print "Creating server ", servname
  print "Server information coming shortly..."
  print ""
  serverinfo = cs.servers.get(server.id)
  while not serverinfo.networks:
    time.sleep(5)
    serverinfo = cs.servers.get(server.id)
  else:    
    network = serverinfo.networks
    print ""
    print "Server Name: ", servname
    print "Server Password: ", root
    print "Server Networks: ", network['public']
    print
    print "--"
  

if __name__ == "__main__":
  arguments = docopt(__doc__)
  main()
