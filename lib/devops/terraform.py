#!/usr/bin/python

import random
from lib.util.library import library as lib

class terraform():
    
    def __init__(self, template, system):
        self.lib        = lib()
        self.lib.readYAML(template)
        self.lib.createDir(template, system)        

    def writeVars(self, source_file):
        dest_file, content = self.lib.getDestFile(source_file) 
        variables          = self.lib.constructVars('variables', 'region', 'vpc', 'subnet', 'ami', 'keypair', 'user')
        with open(dest_file, "w+") as f:
            f.write(content.render(random=random, variables=variables)) 
            
    def writeInstance(self, source_file):
        dest_file, content = self.lib.getDestFile(source_file)
        instance           = self.lib.constructVars('instance', 'name', 'type')
        with open(dest_file, "w+") as f:
            f.write(content.render(instance=instance))

    def writeSG(self, source_file):
        dest_file, content = self.lib.getDestFile(source_file)
        instance           = self.lib.constructVars('instance', 'name')
        security_group     = self.lib.constructVars('security_group', 'prefix', 'description', 'services')
        with open(dest_file, "w+") as f:
            f.write(content.render(instance=instance, security_group=security_group))

    def writeCredentials(self, source_file):
        dest_file, content     = self.lib.getDestFile(source_file)
        access_key, secret_key = self.lib.getAWSCredentials()
        with open(dest_file, "w+") as f:
            f.write(content.render(access_key=access_key, secret_key=secret_key))

    def writeMetaData(self):
        for source in [ "templates/terraform/.gitignore", "templates/terraform/aws_config.tf" ]:
            self.lib.copyFile(source)
    
