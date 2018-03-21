provider "aws" {
  shared_credentials_file = "~/.aws/personal"
  profile                 = "default"
  region                  = "${var.region}"
}