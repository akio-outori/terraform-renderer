#!/usr/bin/python

from os import sys
from lib.aws.ec2_defaults import ec2_defaults
from lib.util.switch import switch

class validate():

    def __init__(self, template, category):
        self.template = template
        self.category = category

    def validate(self, *args):
        if isinstance(self.template[self.category], list):
            self.__validate_list(args)
        else:
            self.__validate_globals(args)

        return self.template[self.category]

    def __validate_globals(self, options):
        for option in options:
            try:
                if self.template[self.category][option] is None:
                    print option + " is blank!  Blank options are not supported."
                    sys.exit(1)

            except KeyError, Argument:
                print "No valid option could be found for " + str(option)
                sys.exit(1)

    def __validate_list(self, options):
        for item in self.template[self.category]:
            for option in options:
                try:
                    if item[option] is None:
                        print option + " is blank!  Blank options are not supported."
                        sys.exit(1)

                except KeyError:
                    try:
                        item[option] = self.__set_defaults(option)
                        if item[option] == None:
                            raise TypeError

                    except TypeError:
                         print "No valid default could be found for " + str(option)
                         sys.exit(1)

    def __set_defaults(self, option):
        default = ec2_defaults(self.template['variables']['region'])
        for case in switch(option):
            if case("vpc"):
                return default.vpc()
            if case("subnet"):
                return default.subnet(self.template['variables']['vpc'])
            if case("ami"):
                return default.ami()
            if case("user"):
                return 'ec2-user'
            if case("name") and category is 'security_groups':
                return 'default_sg'
            if case("services"):
                return ['22']
            else:
                return None





