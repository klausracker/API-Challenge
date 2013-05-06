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

"""cf-delete.py
Cloud Files delete script for customer or racker usage. Prompts for username
and API key, writes these values to an auth file, and will auth using pyrax
to Cloud Files, after first prompting for region and setting a pyrax call
to this region. Will then enumerate the container list for that region
and ask the user to select the container marked for object content deletion.

Usage:
cf-delete.py
cf-delete.py (-h | --help)

Options:
-h --help    Show this help screen.

"""

import pyrax
import sys
import os
from docopt import docopt

def main():

  regionlist = ["DFW", "ORD"]
  
  print
  print "Hello, welcome to the cloud files container purge script."
  print

  def getregion():
    region = str(raw_input ("What region would you like to set? Please use capital letters and the following choices: ( DFW | ORD ) "))
    while region not in ["ORD", "DFW"]:
      print "Invalid region selection, please try again, hint: use capital letters."
      getregion()
    pyrax.set_default_region(region)

  def setcredsanddelete(): 
    print
    username = str(raw_input ("What username would you like to set for your credentials? "))
    print
    apikey = str(raw_input ("What is this user's API key? "))
    try:
      path = os.path.expanduser("~/.customer_cloud_credentials")
      print path
      f = open(path, "wb")
      f.write("[rackspace_cloud]\n")
      f.write("username = " + username + '\n')
      f.write("api_key = " + apikey + '\n')
      f.close() 
    except:
      print
      print "Something happened on the way to writing your file, sorry. Please try again."
      setcreds()
    try:
      creds_file = os.path.expanduser("~/.customer_cloud_credentials")
      pyrax.set_credential_file(creds_file)
    except:
      print
      print "Failed to auth with that username and API key. Perhaps you made a mistake."
      answer = str(raw_input ("Try again? "))
      if (answer == 'Y' or answer == 'y'):
         setcreds()
      else:
         print
         print "Okay, we'll just go ahead and quit for now. Thanks!"
         quit()

    creds_file = os.path.expanduser("~/.customer_cloud_credentials")
    pyrax.set_credential_file(creds_file)
    cf = pyrax.cloudfiles
    print "Here are the containers to choose from"
    print
    contlist = cf.get_all_containers()
    if not contlist:
      print "Sorry, we were not able to find any containers, at least not in this region. Please try your call again later. Goodbye."
      quit()
    else:
      for pos, container in enumerate(contlist, start=1):
        print "%s: %s:" % (pos, container)
      cont_choice = int(raw_input ("Select the container from this list: "))
      cont = contlist[cont_choice - 1]

    cont = cf.get_container(cont)
    print
    print "Are you sure? You are about to delete all content in this container.. procced with caution as this cannot be undone!"
    print
    ans = str(raw_input ("y or n please:  "))
    if (ans == 'Y' or ans == 'y'):
      print
      print "This may take some time ... "
      cont.delete_all_objects()
    else:
      print "Your answer suggested you didn't want to perform this delete, so we're going to bail. Thanks for playing anyway."
      quit()

  getregion()
  setcredsanddelete()

if __name__ == "__main__":
  arguments = docopt(__doc__)
  main()
