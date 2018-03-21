variable "region" {
  default = "us-east-1"
}

variable "aws_vpc" {
  default = "vpc-628dae06"
}

variable "aws_subnet" {
  default = "subnet-9ab7dfa7"
}

variable "ami" {
  default = "ami-1853ac65" 
}

variable "instance_type" {
  default = "t2.medium"
}

variable "aws_keypair" {
  default = "personal"
}

variable "aws_user" {
  default = "ec2-user"
}