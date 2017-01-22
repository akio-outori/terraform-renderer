#!/usr/bin/python

import os
import sys
import yaml
import random
from jinja2 import Template

def createDir():
  if ".yml" in sys.argv[1]:
    ext = sys.argv[1].find('.yml')
  if not os.path.exists(sys.argv[1][0:ext]):
    try:
      os.makedirs(sys.argv[1][0:ext])
      return sys.argv[1][0:ext]
    except:
      return 1

def constructVars():
  region  = data['variables']['region']
  vpc     = data['variables']['vpc']
  subnet  = random.choice(data['variables']['subnet'].values())
  ami     = data['variables']['ami']
  keypair = data['variables']['keypair']
  return region, vpc, subnet, ami, keypair

def writeVars(source_file, dest_dir):
  region, vpc, subnet, ami, keypair = constructVars()
  dest_file = os.path.basename(source_file)
  with open(source_file) as f:
    content = f.read()
  template = Template(content)
  print(template.render(region=region, vpc=vpc, subnet=subnet, ami=ami, keypair=keypair))

def constructInstance():
  instance_name = data['instance']['name']
  instance_type = data['instance']['type']
  return instance_name, instance_type

def constructSg():
  prefix      = data['security_group']['prefix']
  description = data['security_group']['description']
  ports       = data['security_group']['ports']
  return prefix, description, ', '.join(ports)

with open(sys.argv[1]) as f:
  data = yaml.safe_load(f)

dest_dir = createDir()

writeVars('templates/variables.tf', dest_dir)
instance_name, instance_type      = constructInstance()
prefix, description, ports        = constructSg()

print("Instance: ")
print("Instance Name: " + instance_name)
print("Instance Type: " + instance_type)
print("\n")

print("Security Groups: ")
print("Prefix: " + prefix)
print("Description: " + description)
print("Ports: " + ports)
