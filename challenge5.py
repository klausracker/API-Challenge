#!/usr/bin/env python

import pyrax
import time
import sys
import os

pyrax.set_credential_file("~/.rackspace_cloud_credentials")
cdb = pyrax.cloud_databases

def main():
  print "Welcome to the pyrax cloud database creation challenge utility."
  print
  instName = str(raw_input ("What would you like to name your database instance? "))
  instInfo(instName)

def instInfo(instName):
  instance = int(raw_input ("What instance size instance would you like to create? (1 - 4) (1:512MB, 2:1GB, 3:2GB, 4:4GB) "))
  volume = int(raw_input ("What volume in GB (1-50) would you like to start with? "))
  if (instance < 1 or instance > 4) or (volume < 1 or volume > 50):
    print "Incorrect values, please try again. "
    instInfo(instName)
  else:
    dbInfo(instance, volume, instName)

def dbInfo(instance, volume, instName):
  print "So we need to create a database and a user, with a password, in your instance."
  dbName = str(raw_input ("What would you like to call your database? "))
  dbUser = str(raw_input ("What would you like your database user to be named? "))
  dbPass = str(raw_input ("And what would you like your user's password to be? "))
  create(instance, volume, instName, dbName, dbUser, dbPass)

def create(instance, volume, instName, dbName, dbUser, dbPass):
  print "--"
  inst = cdb.create(instName, flavor=instance, volume=volume) 
  time.sleep(5)
  print "Building the instance now, waiting until instance status is active.."
  pyrax.utils.wait_until(inst, 'status', 'ACTIVE', interval=30, verbose=True)  
  dbcreate(inst, dbName, dbUser, dbPass)

def dbcreate(inst, dbName, dbUser, dbPass):
  db = inst.create_database(dbName)
  print "Database created: ", db.name
  user = inst.create_user(dbUser, dbPass, dbName)  
  print "Database user created:", user.name
  print "Remember your password!"
  print
  print "Done!"

if __name__ == "__main__":
  main()
