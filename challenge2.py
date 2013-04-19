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

"""challenge2.py.
Take an image from an existing Rackspace Cloud Server, then build a new
server from this image

Usage:
challenge2.py
challenge2.py (-h | --help)

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

id = "<obfuscated>"
server = cs.servers.get(id)

def main():
  getinfo()

def getinfo():
  print
  imageName = str(raw_input ("What would you like your image to be named? "))
  servName = str(raw_input ("What would you like your new server to be named? "))
  flavSize = str(raw_input ("What flavor size is the original instance (minimum)? "))
  print
  createimage(server, imageName, servName, flavSize)

def createimage(server, imageName, servName, flavSize):
  image_id = server.create_image(imageName)
  buildimage(server, image_id, servName, flavSize)

def buildimage(server, image_id, servName, flavSize):
  image = cs.images.get(image_id)
  if image.status == 'ACTIVE':
    cs.servers.create(servName, image, flavSize)
    print
    print "Building new server", servName, "from", image.name
    print
    print "Done!"
    print
  else:
    time.sleep(15)
    print
    print "Image status is", image.status, "- waiting ..."
    buildimage(server, image_id, servName, flavSize)

if __name__ == "__main__":
  arguments = docopt(__doc__)
  main()
