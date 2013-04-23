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
challenge5.
Create a Database instance, a database, and a user with password , record the
hostname of the instance, and be able to connect remotely to this database as
this user.

Usage:
challenge5.py
challenge5.py (-h | --help)

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

cdb = pyrax.cloud_databases

def main():
  print "Welcome to the pyrax cloud database creation challenge utility."
  print
  instname = str(raw_input ("What would you like to name your database instance? "))
  instinfo(instname)

def instinfo(instname):
  instance = int(raw_input ("What instance size instance would you like to create? (1 - 4) (1:512MB, 2:1GB, 3:2GB, 4:4GB) "))
  volume = int(raw_input ("What volume in GB (1-50) would you like to start with? "))
  if (instance < 1 or instance > 4) or (volume < 1 or volume > 50):
    print "Incorrect values, please try again. "
    instinfo(instname)
  else:
    dbinfo(instance, volume, instname)

def dbinfo(instance, volume, instname):
  print "So we need to create a database and a user, with a password, in your instance."
  dbname = str(raw_input ("What would you like to call your database? "))
  dbuser = str(raw_input ("What would you like your database user to be named? "))
  dbpass = str(raw_input ("And what would you like your user's password to be? "))
  create(instance, volume, instname, dbname, dbuser, dbpass)

def create(instance, volume, instname, dbname, dbuser, dbpass):
  print "--"
  inst = cdb.create(instname, flavor=instance, volume=volume) 
  time.sleep(5)
  print "Building the instance now, waiting until instance status is active.."
  pyrax.utils.wait_until(inst, 'status', 'ACTIVE', interval=30, verbose=True)  
  dbcreate(inst, dbname, dbuser, dbpass)

def dbcreate(inst, dbname, dbuser, dbpass):
  db = inst.create_database(dbname)
  print "Database created: ", db.name
  user = inst.create_user(dbuser, dbpass, dbname)  
  print "Database user created:", user.name
  print "Remember your password!"
  print
  print "Done!"

if __name__ == "__main__":
  arguments = docopt(__doc__)
  main()
