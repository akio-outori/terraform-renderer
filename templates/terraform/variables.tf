variable "access_key" {}

variable "secret_key" {}

variable "aws_region" {
  default = "{{ variables['region'] }}"
}

