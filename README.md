# terraform-renderer

This is a utility I designed to help with standing up AWS test systems.  Currently, the util takes parameters in a YAML file to 
generate a terraform plan for your environment.  This can be done on a per system basis, with per cluter support TBD.  Usage is 
outlined below:

## Configuration 

Global configuration is supplied via the included ```config.yml``` file.  Supported configuration options are:

* **terraform_dir** (required): Directory where terraform plans are stored once generated.  Each plan will be stored in a folder matching the name of configuration file used.
* **configuration_dir** (required): Directory where YAML configuration files are stored.  Any configuration file used with the ```generator``` command will be copied into this directory.

## Basic Usage

Terraform plans are generated using the ```generator``` tool provided in this repository.  The tool should be run from the top level of this repository and requires the lib and templates directories to function properly.  The environments folder is included only as an example, and could be replaced with anything by changing the configuration options outlined in the section above.

Basic usage is as follows:

```./generator <option> <file>```

Where:
* **option** - The action to take, e.g. createAll, createSG, etc
* **file** - The path to a .yml template to use for generation  

Currently supported options are:
```
$ ./generator 
Option not understood:
  createAll
  createCredentials
  createInstance
  createVars
  createSG

usage: generator <option> <file>.yml 
```

## Parameters

YAML templates for use with the tool should take the following format:

```
---

- environment: "production"

  variables:
    region: "us-east-1"
    vpc: "vpc-xxxxxxxx"

  instances:
    
    - name: "test"
      type: "t2.micro"
      user: "centos"
      keypair: "test"
      security_group: "generator-test"

    - name: "test2"
      type: "t2.micro"
      user: "centos"
      keypair: "test"
      security_group: "generator-test"

  security_groups:

    - name: "generator-test"
      description: "test sg for terraform auto-generation"

```

### Variables

General variables for the variables.tf template.  Currently the following options are supported:

* **region** (**required**): AWS region
* **vpc** (optional): VPC ID for the region listed.  If this is not supplied, the utility will attempt to use your default VPC.
* **bastion_host** (optional): Hostname of the SSH gateway to use with terraform if required.
* **bastion_user** (optional): SSH user for the proxy host defined in ```bastion_user```.

### Instance

Instance variables specified in the instance.tf template.  This file will be copied to a file matching the instance name for each defined instance.  Currently the following options are supported:

* **name** (**required**): Instance name to be used.  Can be an arbitrary name / string
* **type** (**required**): Instance type to be created, see the AWS documentation [here](https://aws.amazon.com/ec2/instance-types/) for a breakdown on possible types.
* **keypair** (**required**): EC2 keypair to be used when launching the instance.
* **security_group** (**required**): Security group to assign at launch.
* **user** (optional): SSH user for the created instance.  Defaults to ec2-user if not supplied.
* **ami** (optional): System image to be used when spinning up the instance.  If this option is blank, the tool will attempt to use the most recent amazon linux AMI.
* **subnet** (optional): A set of key value pairs listing possible subnets to launch the instance into.  The option should take the following format:

```
subnet:
  example1: "subnet-xxxxxxxx"
  example2: "subnet-xxxxxxxx"
```

If more than one subnet is defined, the configured subnet will be chosen at random from the configured options.If this option is not present the tool will attempt to set the default public subnet for the configured VPC.

* **associate_public_ip** (optional):  True/False value that determines whether a public IP should be initially assigned to the host.  This can be helpful when installation scripts require internet access.
* **config_script** (optional): Configuration script to run as part of post-install.  This script should be copied to the instance using ```config_files```.
* **config_dir** (**required if ```config_files``` is set**): Remote directory on the instance where all configuration files listed in ```config_files``` will be stored.
* **config_files** (optional): A list of local files to be copied to the instance as part of configuration.  This should be defined as follows:

```
config_files:
  - "test.sh"
  - "test2.sh"
```

### Security Groups

Security group variables specified in security_group.tf.  Currently the following options are supported:

* **name** (**required**): Name of the security group to be created.
* **description** (**required**): Description for the security group.  Can be a descriptive string / name.
* **prefix** (optional): Prefix for the auto-generated security group.  Please see terraform documentation [here](https://www.terraform.io/docs/providers/aws/r/security_group.html) for more info on ```name_prefix```.  This will be used instead of ```name``` when specified.
* **services** (**required**): List of services to add to ingress for the security group.  This option can take two forms:

#### Services Open to the World

If no ip address restrictions are needed, services can simply be a list of ports to open to 0.0.0.0/0:

```
- name: "test"
  description: "test sg for terraform auto-generation"
  services:
    - "22"
    - "80"
    - "443"
```
#### Restricted Services

If more robust SG restrictions are needed, services can be a list of services with *port*, *range*, and *protocol* specified:

```
- name: "test"
  description: "test sg for terraform auto-generation"
  services:
    ssh:
      port: "22"
      range: "192.168.1.0/24"
      protocol: "tcp"
    http:
      port: "80"
      range: "0.0.0.0/0"
      protocol: "tcp"
    https:
      port: "443"
      range: "0.0.0.0/0"
      protocol: "tcp"
``` 
