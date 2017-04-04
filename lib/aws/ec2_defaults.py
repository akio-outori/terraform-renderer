#!/usr/bin/python

import boto3
import datetime

class ec2_defaults():

    def __init__(self, region):
        self.ec2     = boto3.resource('ec2', region_name=region)
        self.client  = boto3.client('ec2')
        self.filters = [{'Name':'tag:Name', 'Values':['*']}]

    def vpc(self):
        vpcs    = list(self.ec2.vpcs.filter(Filters=self.filters))
        for vpc in vpcs:
            if vpc.is_default is True:
                return vpc.id

    def subnet(self, vpc):
        subnets = list(self.ec2.subnets.filter(Filters=self.filters))
        for subnet in subnets:
            if subnet.vpc_id == vpc and subnet.map_public_ip_on_launch is True:
                return { 'default': subnet.id }

    def ami(self):
        filters = [
                {'Name':'architecture', 'Values':['x86_64']}, 
                {'Name':'virtualization-type', 'Values':['hvm']}, 
                {'Name':'is-public', 'Values':['true']}, 
                {'Name':'owner-alias', 'Values':['amazon']}, 
                {'Name':'image-type', 'Values':['machine']}, 
                {'Name':'hypervisor', 'Values':['xen']},
                {'Name':'block-device-mapping.volume-type', 'Values':['standard']},
                {'Name':'description', 'Values':["*Amazon Linux*"]}
        ]

        images  = list(self.ec2.images.filter(Filters=filters))
        current = datetime.datetime.now()

        for image in images:
            if str(current.year) in image.creation_date and "rc" not in image.description:
                return image.id

