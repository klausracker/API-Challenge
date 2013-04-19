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

"""challenge3.py.

Usage: 
  challenge3.py (-h | --help)
  challenge3.py PATH_TO_FILES CONTAINER_NAME

Arguments:
  PATH_TO_FILES    The directory path to your files you wish to upload
  CONTAINER_NAME   The container name you wish to upload your files into

Options:
  -h --help   Show this help screen

"""

import pyrax
import sys
import os
from docopt import docopt

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)

cf = pyrax.cloudfiles

def main():
  print "Hello, about to upload your files into a container. Hopefully."
  localdir = sys.argv[1]
  contname = sys.argv[2]
  checkargs(localdir, contname)

def checkargs(localdir, contname):
  count = 0
  print "Checking to see if you passed your path as your container. Hoping you didn't use any slashes '/' in your container name"
  for i in contname:
    if i == '/':
      if count == 1:
        print "Slashes found in both arguments. Can't tell which is your path. I'm going to fail. Sorry."
        quit()
      print "Directory structure discovered. You may have passed your path as your container. Flipping your choices and trying again"
      contname, localdir = localdir, contname
      count += 1
      checkargs(localdir, contname)
  else:
    createcont(localdir, contname)

def createcont(localdir, contname):
  cont = cf.create_container(contname)
  print "Creating container ", cont.name, "if it doesn't already exist."
  print "If it does exist, we'll just write into the existing container."
  testpath(cont, localdir)

def testpath(cont, localdir):
  if os.path.isdir(localdir) == True:
    print "Valid path, uploading files.."
    uploadfiles(cont, localdir)
  else:
    localdir = str(raw_input ("This is not a valid path, please try again: "))
    testpath(cont, localdir)

def uploadfiles(cont, localdir):
  cont = cf.upload_folder(localdir, cont.name)    
  print "Done!"

if __name__ == "__main__":
  arguments = docopt(__doc__)
  main()
