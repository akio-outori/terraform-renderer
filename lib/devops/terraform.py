#!/usr/bin/python

import random
import os
import sys
from lib.util.parse_yaml import read as read_yaml
from lib.util.files import mkdir, cp, read 
from lib.util.validate import validate
from lib.util.template import read as read_template
from lib.util.aws import getCredentials

class terraform():
    
    def __init__(self, template):
        self.template   = read_yaml(template)
        self.parent_dir = self.__makeEnv('config.yml', template)

        self.__validate()

    def __validate(self):
        validate_vars      = validate(self.template[0], 'variables')
        validate_instances = validate(self.template[0], 'instances')
        validate_sg        = validate(self.template[0], 'security_groups')

        self.variables     = validate_vars.validate('region', 'vpc')
        self.instances     = validate_instances.validate('name', 'type', 'subnet', 'ami', 'keypair', 'user')
        self.sg            = validate_sg.validate('name', 'services')

    def __makeEnv(self, config, template):
        config        = read_yaml(config)
        template_path = os.path.splitext(os.path.basename(template))[0]
        for option, path in config.iteritems():
            mkdir(path) 

        cp(template, config['configuration_dir']) 
        return mkdir(config['terraform_dir'] + '/' + template_path)

    def __makeDestFile(self, source_file):
        return self.parent_dir + '/' + os.path.basename(source_file)

    def writeVars(self, source_file):
        content       = read_template(source_file)
        dest_file     = self.__makeDestFile(source_file)
        with open(dest_file, "w+") as f:
            f.write(content.render(variables=self.variables)) 
            
    def writeInstance(self, source_file):
        content    = read_template(source_file)
        for instance in self.instances:
            dest_file  = self.__makeDestFile(instance['name'] + '.tf')
            with open(dest_file, "w+") as f:
                f.write(content.render(os=os, random=random, instance=instance, variables=self.variables))

    def writeSG(self, source_file):
        content         = read_template(source_file)
        dest_file       = self.__makeDestFile(source_file)
        with open(dest_file, "w+") as f:
            f.write(content.render(security_groups=self.sg, variables=self.variables))

    def writeCredentials(self, source_file):
        content                = read_template(source_file)
        dest_file              = self.__makeDestFile(source_file)
        access_key, secret_key = getCredentials()
        with open(dest_file, "w+") as f:
            f.write(content.render(access_key=access_key, secret_key=secret_key))

    def writeMetaData(self):
        for source in [ "templates/terraform/.gitignore", "templates/terraform/aws_config.tf" ]:
            cp(source, self.parent_dir)
    
