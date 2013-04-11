import pyrax
import sys

pyrax.set_credential_file("/Users/kevi4546/.rackspace_cloud_credentials")
cdb = pyrax.cloud_databases

instances = cdb.list()
if not instances:
    print "There are no cloud database instances."
    print "Please create one and re-run this script."
    sys.exit()

print
print "Available Instances:"
for pos, inst in enumerate(instances):
    print "%s: %s (%s, RAM=%s, volume=%s) Status=%s" % (pos, inst.name,
            inst.flavor.name, inst.flavor.ram, inst.volume.size, inst.status) 
