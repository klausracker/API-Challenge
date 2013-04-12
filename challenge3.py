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
import sys
import os

pyrax.set_credential_file("~/.rackspace_cloud_credentials")

cf = pyrax.cloudfiles

def main():
  createcont()

def createcont():
  print "Hello, about to upload your files into a container. Hopefully."
  cont = cf.create_container(sys.argv[2])
  print "Creating container ", cont.name, "if it doesn't already exist."
  print "If it does exist, we'll just write into the existing container."
  localdir = sys.argv[1]
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
  main()
