variable "access_key" {}

variable "secret_key" {}

variable "aws_region" {
  default = "{{ region }}"
}

variable "aws_vpc" {
  default = "{{ vpc }}"
}

variable "aws_subnet" {
  default = "{{ subnet }}"
}

variable "ami" {
  default = "{{ ami }}"
}

variable "aws_keypair" {
  default = "{{ keypair }}"
}

variable "aws_user" {
  default = "{{ user }}"
}
