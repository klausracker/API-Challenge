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

"""challenge10.py.
Create two servers, upload an SSH RSA key, then create a load balancer, add 
the two servers to the load balancer, then create an A record for the FQDN to
the load balancer's public IP address. Make a custom error document and  
upload this document to Cloud Files to be served. Create a monitoring check.


Usage:
challenge10.py (-h | --help)
challenge10.py NAME PATHTOFILE FQDN


Arguments:
NAME          The desired server name prefix
PATHTOFILE    The path to your SSH key you wish to upload to your server
FQDN          The FQDN you wish to set the Load Balancer Public IP address to


Options:
-h --help     Show this help screen

"""

import pyrax
import time
import sys
import os
import whois
from docopt import docopt
import base64
import struct
from html import HTML

cred_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(cred_file)

cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
image = "da1f0392-8c64-468f-a839-a9e56caebf07"


def main():
  chkargs()

def chkargs():
  name = sys.argv[1]
  pathtofile = sys.argv[2]
  fqdn = sys.argv[3]

  try:
    os.path.isfile(pathtofile)
    print
    print "Looks like a valid file, going to try to validate the file as an actual SSH key"
  except:
    print
    print "Not a valid path or file, please try again"
    quit()

  with open(pathtofile,'r') as f:
    file = f.read()
  try:
    type, key_string, comment = file.split() 
    data = base64.decodestring(key_string)
    str_len = struct.unpack('>I', data[:4])[0] # this should return 7
    data[4:4+str_len] == type
  except:
    print "File didn't prove itself to be an SSH key. Please try again."
    quit()
  f.close()

  if type == 'ssh-rsa':
    print
    print "Seems like a valid SSH RSA key. Let's continue some more and see what happens."
  else:
    print
    print "Sorry, I didn't find an SSH RSA key. What I found was", type, "and this isn't right. Please try again"
    quit()

  try:
    w = whois.whois(fqdn)
  except:
    print
    print "This doesn't seem to be a FQDN. Please try again."
    quit()

  print
  print "Proceeding with creating your servers."
  createservers(name, fqdn, file)

def createservers(name, fqdn, file):
  files = {"/root/.ssh/authorized_keys": file}
  servname1 = name + str(1)
  servname2 = name + str(2)
  server1 = cs.servers.create(servname1, image, "2", files=files)
  root1 = server1.adminPass
  server2 = cs.servers.create(servname2, image, "2", files=files)
  root2 = server2.adminPass
  print
  print "Servers created, just waiting for networking information. This may take some time.."
  print
  while not (server1.networks and server2.networks):
    time.sleep(2)
    server1 = cs.servers.get(server1.id)
    server2 = cs.servers.get(server2.id)
  print
  print "Your server information is:"
  print
  print server1.name, "@", server1.networks["public"], "with root password", root1
  print server2.name, "@", server2.networks["public"], "with root password", root2
  print
  createload(server1, server2, fqdn)

def createload(server1, server2, fqdn):
  print
  print "Now we need to create your custom error document."
  content = str(raw_input ("What content would you like to add into this file? "))
  tags = str(raw_input ("What tags would you like to enclose this text with? (We'll add the brackets and slashes for you) "))
  text = HTML(tags)
  text(content)
  print
  print "Creating load balancer and adding custom error document."

  server1_ip = server1.networks["private"][0]
  server2_ip = server2.networks["private"][0]
 
  node1 = clb.Node(address=server1_ip, port=80, condition="ENABLED")
  node2 = clb.Node(address=server2_ip, port=80, condition="ENABLED")

  vip = clb.VirtualIP(type="PUBLIC")
  lb = clb.create(fqdn, port=80, protocol="HTTP", nodes=[node1, node2], virtual_ips=[vip])
  pyrax.utils.wait_until(lb, 'status', 'ACTIVE', interval=10, verbose=True)
  lb.add_health_monitor(type="HTTP", delay=10, timeout=10,
        attemptsBeforeDeactivation=3, path="/",
        statusRegex="^[234][0-9][0-9]$",
        bodyRegex=".* testing .*",
        hostHeader=fqdn)
  lb.set_error_page(str(text))

  print "Your load balancer", loadname, "has been created with nodes", server1.name, "and", server2.name
  uploadfile(errorfile, text)
  createdns(vip, fqdn)

def createdns(ip, fqdn):
  print
  print "Setting the DNS entry for the FQDN to the load balancer's VIP."
  print
  ttl = str(raw_input ("What value would you like to set your TTL for this DNS record to? "))

  record = [{"type": "A",
            "name": fqdn,
            "data": ip,
            "ttl": ttl,
            }]

  try:
    newrecord = dns.add_record(record)
  except:
    print "Domain doesn't exist to add a record, tryiing to create it."
    email = str(raw_input ("What administrative email would you like to set for this domain? "))
    newrecord = dns.create(name=fqdn, emailAddress=email)
  finally:
    print "Well that didn't work, check existing records for this domain. Gonna quit for now."
    quit()

def uploadfile(errorfile, text):
  print
  print "Backing up your error document to a cloud files folder now."
  contname = str(raw_input ("And what would you like to name the container to upload this file into? "))
  cont = cf.create_container(contname)
  print "Creating container ", contname, "if it doesn't already exist."
  print "If it does exist, we'll just write into the existing container."
  print
  cont = cf.get_container(contname)
  obj = cf.store_object(cont, "error_page.html", str(text))

if __name__ == "__main__":
  arguments = docopt(__doc__)
  main()
