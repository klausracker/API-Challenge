import pyrax
import os

cred_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(cred_file)

dns = pyrax.cloud_dns
ip =  '166.78.41.13'
doma = str(raw_input ("Domain: "))
ttl = 900 
try:
  dom = dns.find(name=doma)
  print "Domain found"
except:
  print "Domain not found"

record = [{"type": "A",
          "name": doma,
          "data": ip,
          "ttl": ttl,
          }]
print record
dom.add_records(record)

