#!/usr/bin/python

from os import sys
from lib.aws.ec2_defaults import ec2_defaults

def validate(template, category, *args):
    for option in args:
        try:
            if template[category][option] is None:
                print option + " is blank!  Blank options are not supported."
                sys.exit(1)
        
        except KeyError, Argument:
            try:
                default = ec2_defaults(template['variables']['region'])
                
                if option is 'vpc':
                    template[category][option] = default.vpc()
                elif option is 'subnet':
                    template[category][option] = default.subnet(template['variables']['vpc'])
                elif option is 'ami':
                    template[category][option] = default.ami()
                elif option is 'user':
                    template[category][option] = "ec2-user"
                    
                if template[category][option] == None:
                    raise TypeError
            
            except TypeError:
                print "No valid default could be found for " + str(option)
                sys.exit(1)
            
    return template[category]
