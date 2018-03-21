provider "aws" {
  shared_credentials_file = "{{ variables['credentials']['credential_file'] }}"
  profile                 = "{{ variables['credentials']['profile'] }}"
  region                  = "${var.region}"
}
