import pyrax
import time
import sys
import os

pyrax.set_credential_file("~/.rackspace_cloud_credentials")
cs = pyrax.cloudservers

id = "<obfuscated>"
server = cs.servers.get(id)

def main():
  getinfo()

def getinfo():
  print
  imageName = str(raw_input ("What would you like your image to be named? "))
  servName = str(raw_input ("What would you like your new server to be named? "))
  flavSize = str(raw_input ("What flavor size is the original instance (minimum)? "))
  print
  createImage(server, imageName, servName, flavSize)

def createImage(server, imageName, servName, flavSize):
  image_id = server.create_image(imageName)
  buildImage(server, image_id, servName, flavSize)

def buildImage(server, image_id, servName, flavSize):
  image = cs.images.get(image_id)
  if image.status == 'ACTIVE':
    cs.servers.create(servName, image, flavSize)
    print
    print "Building new server", servName, "from", image.name
  else:
    time.sleep(15)
    print
    print "Image status is", image.status, "- waiting ..."
    buildImage(server, image_id, servName, flavSize)

if __name__ == "__main__":
  main()
