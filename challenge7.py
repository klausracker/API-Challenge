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
clb = pyrax.cloud_loadbalancers
image = "c195ef3b-9195-4474-b6f7-16e5bd86acd0"


def main():
  info()

def info():
  print "Hello, we're about to create two servers attached to a cloud load balancer."
  print
  prename = str(raw_input ("What would you like to call your servers? "))
  servname1 = prename + str(1)
  servname2 = prename + str(2)  
  loadname = str(raw_input ("What would you like to call your load balancer? "))
  createservers(servname1, servname2, loadname)

def createservers(servname1, servname2, loadname):
  server1 = cs.servers.create(servname1, image, "2")
  root1 = server1.adminPass
  server2 = cs.servers.create(servname2, image, "2")
  root2 = server2.adminPass
  print "Creating servers and waiting for networking information. This may take some time.."
  print 
  createload(server1, server2, loadname)
  print "Your load balancer", loadname, "has been created with nodes", server1.name, "and", server2.name
  printinfo(server1, server2, root1, root2)

def createload(server1, server2, loadname):
  while not (server1.networks and server2.networks):
    time.sleep(1)
    server1 = cs.servers.get(server1.id)
    server2 = cs.servers.get(server2.id)

  server1_ip = server1.networks["private"][0]
  server2_ip = server2.networks["private"][0]

  node1 = clb.Node(address=server1_ip, port=80, condition="ENABLED")
  node2 = clb.Node(address=server2_ip, port=80, condition="ENABLED")

  vip = clb.VirtualIP(type="PUBLIC")
  lb = clb.create(loadname, port=80, protocol="HTTP", nodes=[node1, node2], virtual_ips=[vip])

def printinfo(server1, server2, root1, root2):
  server1 = cs.servers.get(server1.id)
  server2 = cs.servers.get(server2.id)
  print
  print "Your server information is:"
  print
  print server1.name, "@", server1.networks["public"], "with root password", root1
  print server2.name, "@", server2.networks["public"], "with root password", root2
  print    
  print "Done!"
  print

if __name__ == "__main__":
  main()
