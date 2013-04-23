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

"""challenge9.py.
Build a server from a desired image, name it based upon a FQDN, then assign a DNS A record 
from the server's public IPv4 address to the same FQDN.

Usage:
challenge9.py (-h | --help)
challenge9.py FQDN IMAGE FLAVOR

Arguments:
FQDN     The Fully Qualified Domain Name. Must be a registered domain name. 
IMAGE    The 36 character Rackspace image ID to build the server from
FLAVOR   The flavor size (2 - 8) in which to create your server instance

Options:
-h --help    Show this help screen. 

"""

import pyrax
import time
import sys
import os
import pyrax.exceptions as exc
import whois
from docopt import docopt

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)

cs = pyrax.cloudservers
dns = pyrax.cloud_dns

def main():
  checkargs()

def checkargs():
  
  fqdn = sys.argv[1]
  image = sys.argv[2]
  flavor = sys.argv[3]

  try:
    img = cs.images.get(image)
    print "Good news, we found a valid image, continuing.."
  except:
    print "Sorry, your image was not found in the image list. Please try again."
    quit()

  try:
    int(flavor)
  except:
    print "Your flavor input was not numeric. Please try again."
    quit()

  try:
    cs.flavors.get(flavor)
    print "Valid flavor, still continuing"
  except:
    print "Your flavor is out of range. Please try again."
    quit()

  try:
    w = whois.whois(fqdn)
    print "Seems like a valid FQDN, let's keep rolling.."
  except:
    print
    print "This domain isn't a FQDN, please choose one that is. Quitting now."
    quit() 

  create(fqdn, image, img, flavor)

def create(fqdn, image, img, flavor):
  print
  print "Creating server with name", fqdn, "from", img, "of flavor size", flavor
  print "then creating a DNS entry to the public IP. Wish me luck!"

  server = cs.servers.create(fqdn, image, flavor)
  serverinfo = cs.servers.get(server.id)

  print
  print "Bulding server and waiting on networking information.."
  while not serverinfo.networks:
    time.sleep(1)
    serverinfo = cs.servers.get(server.id)
  getaddresses(server, fqdn)

def getaddresses(server, fqdn):
  serverinfo = cs.servers.get(server.id)
  public = serverinfo.networks['public']
  for address in public:
    if len(address) < 20:
      ip = address
  adddns(ip, fqdn)

def adddns(ip, fqdn):
  print
  print "Assigning the DNS entry now. Hopefully.."

  record = [{"type": "A",
            "name": fqdn,
            "data": ip,
            "ttl": 900,
            }]

  try:
    dom = dns.find(name=fqdn)
  except:
    print
    print "Domain not found, creating.."
    email = str(raw_input ("Please enter in an administrative email for this new domain: "))
    try:
      dom = dns.create(name=fqdn, emailAddress=email)
    except exc.DomainCreationFailed as e:
        print "Domain creation failed: domain may be owned elsewhere.", e
        quit()
    print 
    print "Domain creation successful!"
  
  newrecord = dom.add_records(record)
     
  print
  print "Done!"


if __name__ == "__main__":
  arguments = docopt(__doc__)
  main()
