variable "access_key" {}

variable "secret_key" {}

variable "aws_region" {
  default = "{{ variables['region'] }}"
}

variable "aws_vpc" {
  default = "{{ variables['vpc'] }}"
}

variable "aws_subnet" {
  default = "{{ random.choice(variables['subnet'].values()) }}"
}

variable "ami" {
  default = "{{ variables['ami'] }}"
}

variable "aws_keypair" {
  default = "{{ variables['keypair'] }}"
}

variable "aws_user" {
  default = "{{ variables['user'] }}"
}
