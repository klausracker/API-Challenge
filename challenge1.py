#!/usr/bin/env python

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

