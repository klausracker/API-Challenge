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

"""
challenge6.py.
Create, and then CDN enable a cloud files container.

Usage:
challenge.py
challenge.py (-h | --help)

Options:
-h --help    Show this screen

"""

import pyrax
import sys
import os
from docopt import docopt

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)

cf = pyrax.cloudfiles

def main():
  createcont()

def createcont():
  print "Hello, about to create a CDN enabled container."
  print
  contname = str(raw_input ("What would you like to call this container? "))
  cont = cf.create_container(contname)
  print "Creating container ", cont.name, "if it doesn't already exist."
  print "If it does exist, we'll just enable the existing container."
  print
  ttl = str(raw_input ("What TTL value would you like to set for this public container? ")) 
  enablecont(cont, contname, ttl)

def enablecont(cont, contname, ttl):
  cont = cf.make_container_public(cont.name, ttl=ttl)
  print
  print "Done!"

if __name__ == "__main__":
  arguments = docopt(__doc__)
  main()
