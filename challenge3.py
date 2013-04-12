#!/usr/bin/env python

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
