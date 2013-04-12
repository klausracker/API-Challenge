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

import pyrax
import time
import sys
import os

pyrax.set_credential_file("~/.rackspace_cloud_credentials")
cs = pyrax.cloudservers

def create(servName):
  image = "c195ef3b-9195-4474-b6f7-16e5bd86acd0"
  server = cs.servers.create(servName, image, "2")
  root = server.adminPass
  print "Creating server ", servName
  print "Server information coming shortly..."
  print ""
  getInfo(servName, server, root)

def getInfo(servName, server, root):
  serverinfo = cs.servers.get(server.id)
  while not serverinfo.networks:
    time.sleep(5)
    getInfo(servName, server, root)
  else:    
    network = serverinfo.networks
    print ""
    print "Server Name: ", servName
    print "Server Password: ", root
    print "Server Networks: ", network['public']
    print "--"

i = 1
print ""
preName = str(raw_input ("What would you like your servers to be named? "))
print ""
serverCount = int(raw_input ("How many servers would you like to create? "))

while i <= serverCount:
  servName = preName + str(i)
  create(servName)
  i += 1

