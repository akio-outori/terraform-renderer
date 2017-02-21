# terraform-renderer

This is a utility I designed to help with standing up AWS test systems.  Currently, the util takes parameters in a YAML file to 
generate a terraform plan for your environment.  This can be done on a per system basis, with per cluter support TBD.  Usage is 
outlined below:

## Basic Usage

Terraform plans are generated using the ```generator``` tool provided in this repository.  The tool requires the contents of the
includes and templates directories to function properly.  The environments folder is included only as an example, and could be 
replaced with anything.

Basic usage is as follows:

```./generator <option> <file> <system>```

Where:
* **option** - The action to take, e.g. createAll, createSG, etc
* **file** - The path to a .yml template to use for generation
* **system** - The name of the system to be created.  

Currently supported options are:
```
$ ./generator 
Option not understood:
  createAll
  createCredentials
  createInstance
  createVars
  createSG

usage: generator <option> <file>.yml <system>
```

## Parameters

YAML templates for use with the tool should take the following format:

```
---

variables:
  region: "region"
  vpc: "vpc"
  subnet: 
    east-1a: "subnet-1a" 
    east-1b: "subnet-1b"
    east-1c: "subnet-1c"
    east-1d: "subnet-1d"
  ami: "ami"
  user: "ec2-user"
  keypair: "some-keypair"

instance:
  name: "test"
  type: "t2.micro"
  
security_group:
  prefix: "yaml-test"
  description: "test sg for terraform auto-generation"
  services:
    - "22"
    - "80"
    - "443"
```

### Variables

General variables for the variables.tf file.  Currently the following options are supported:

* **region** (required): AWS region
* **vpc** (required): VPC ID for the region listed
* **subnet** (required): list of subnets.  **The util will choose a random subnet from the list.**
* **ami** (required): AWS AMI ID to be used
* **keypair** (required): AWS keypair to be used.  **Note that this keypair should also exist on your local system.**

### Instance

Instance variables specified in the instance.tf file.  Currently the following options are supported:

* **name** (required): Instance name to be used.  Can be an arbitrary name / string
* **type** (required): Instance type to be created, see the AWS documentation [here](https://aws.amazon.com/ec2/instance-types/) for a breakdown on possible types.

### Security Groups

Security group variables specified in security_group.tf.  Currently the following options are supported:

* **prefix** (required): Prefix for the auto-generated security group.  Please see terraform documentation [here](https://www.terraform.io/docs/providers/aws/r/security_group.html) for more info on ```name_prefix```.
* **description** (required): Description for the security group.  Can be a descriptive string / name.
* **services** (required): List of services to add to ingress for the security group.  This option can take two forms:

#### Services Open to the World

If no ip address restrictions are needed, services can simply be a list of ports to open to 0.0.0.0/0:

```security_group:
prefix: "yaml-test"
description: "test sg for terraform auto-generation"
services:
  - "22"
  - "80"
  - "443"
```
#### Restricted Services

If more robust SG restrictions are needed, services can be a list of services with *port*, *range*, and *protocol* specified:

```
security_group:
  prefix: "yaml-test"
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
