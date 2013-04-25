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

"""challenge8.py.
Create a static webpage to be served from a cloud files container. Create
a container, CDN enable it, enable to serve a default document, upload
the document and create a CNAME entry to the CDN URL.

Usage:
challenge8.py
challenge8.py (-h | --help)

Options:
-h --help    Show this help screen.

"""

import pyrax
import sys
import os
from html import HTML
from docopt import docopt

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)

cf = pyrax.cloudfiles
dns = pyrax.cloud_dns


def main():
  indexinfo()

def indexinfo():
  default = str(raw_input ("what would you like to call your default document? We'll append the .html " ))
  index = default + ".html"
  content = str(raw_input ("What content would you like to add into this file? "))
  tags = str(raw_input ("What tags would you like to enclose this text with? (We'll add the brackets and slashes for you) "))

  text = HTML(tags)
  text(content)
  createcont(index, text)

def createcont(index, text):
  contname = str(raw_input ("And what would you like to name the container to upload this file into? "))
  cont = cf.create_container(contname)
  print "Creating container ", contname, "if it doesn't already exist."
  print "If it does exist, we'll just write into the existing container."
  print
  print "Setting metadata for container.. "
  new_meta = {"X-Container-Meta-Web-Index": index}
  cont = cf.set_container_metadata(contname, new_meta)
  print
  ttl = str(raw_input ("What TTL value would you like to set for this public container? (900 minimum) "))
  cont = cf.make_container_public(contname, ttl=ttl)
  cont = cf.get_container(contname)
  url = cont.cdn_uri[7:]
  print
  print "Publishing your default html document to your CDN enabled container.. "

  obj = cf.store_object(contname, index, str(text))
  setcname(url, ttl)

def setcname(url, ttl):
  print
  print "Here are your domains to select from: "
  domainlist = dns.list()
  for pos, domain in enumerate(domainlist, start=1):
    print "%s: %s" % (pos, domain.name)
  dom_choice = int(raw_input ("Select your domain to set your CNAME from this list: "))
  domain = domainlist[dom_choice - 1]

  print
  sub = str(raw_input ("What would you like your CNAME to be? "))
  subdomain = sub + "." + domain.name

  record = [{"type": "CNAME",
          "name": subdomain,
          "data": url,
          "ttl": ttl,
          }]

  cname = domain.add_records(record)
  
  print
  print "Done!"


if __name__ == "__main__":
  arguments = docopt(__doc__)
  main()
