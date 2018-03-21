variable "region" {
  default = "{{ variables['environment']['region'] }}"
}

variable "aws_vpc" {
  default = "{{ variables['environment']['vpc'] }}"
}

variable "aws_subnet" {
  default = "{{ variables['environment']['subnet'] }}"
}

variable "ami" {
  default = "{{ variables['instance']['ami'] }}" 
}

variable "instance_type" {
  default = "{{ variables['instance']['instance_type'] }}"
}

variable "aws_keypair" {
  default = "{{ variables['instance']['keypair'] }}"
}

variable "aws_user" {
  default = "{{ variables['instance']['user'] }}"
}
