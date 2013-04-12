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
import socket

pyrax.set_credential_file("~/.rackspace_cloud_credentials")
dns = pyrax.cloud_dns

def main():
  print "Here are your domains to select from: "
  domainlist = dns.list()
  for pos, domain in enumerate(domainlist, start=1):
    print "%s: %s" % (pos, domain.name)
  dom_choice = int(raw_input ("Select your domain from this list: "))
  domain = domainlist[dom_choice - 1]
  isAddress(dns, domain)

def isAddress(dns, domain):
  ipaddr = str(raw_input ("Please enter the desired IPv4 address for your DNS A record: "))
  try:
    addr = socket.inet_pton(socket.AF_INET, ipaddr)
  except AttributeError:
    try:
      addr = socket.inet_aton(ipaddr)
    except socket.error:
      print "Not a valid IPv4 address, please try again: "
      isAddress(dns, domain)
    return address.count('.') == 3
  except socket.error:
    print "Not a valid IPv4 address, please try again: "
    isAddress(dns, domain)     
  addRecord(dns, domain, ipaddr) 

def addRecord(dns, domain, ipaddr):
  print
  print "Adding record ... "
  try:
    rec = [{"type": "A", "name": domain.name, "data": ipaddr, "ttl": 6000}] 
    dns.add_records(domain, rec)
    print "Created record for", domain.name, "with A record", ipaddr
  except:
    print "Something didn't work right, try again "
    quit()

if __name__ == "__main__":
  main()
