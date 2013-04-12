#!/usr/bin/env python

import pyrax
import sys

pyrax.set_credential_file("~/.rackspace_cloud_credentials")

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
  main()
