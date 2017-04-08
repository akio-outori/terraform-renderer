#!/usr/bin/python

from os import sys
from lib.aws.ec2_defaults import ec2_defaults

def validate(template, category, *args):
    if isinstance(template[category], list):
        for item in template[category]:
            for option in args:
                try:
                    if item[option] is None:
                        print option + " is blank!  Blank options are not supported."
                        sys.exit(1)

                except KeyError, Argument:
                    default = ec2_defaults(template['variables']['region'])
                    
                    if option is 'vpc':
                        item[option] = default.vpc()
                    elif option is 'subnet':
                        item[option] = default.subnet(template['instance']['vpc'])
                    elif option is 'ami':
                        item[option] = default.ami()
                    elif option is 'user':
                        item[option] = "ec2-user"
                    elif option is 'prefix':
                        item[option] = template['instance']['name']
                    elif option is 'services':
                        item[option] = ['22']
                        
                    if item[option] == None:
                        raise TypeError
                    
                except TypeError:
                    print "No valid default could be found for " + str(option)
                    sys.exit(1)


    else:
        for option in args:
            try:
                if template[category][option] is None:
                    print option + " is blank!  Blank options are not supported."
                    sys.exit(1)

            except KeyError, Argument:
                print "No valid option could be found for " + str(option)
                sys.exit(1)

    return template[category]


