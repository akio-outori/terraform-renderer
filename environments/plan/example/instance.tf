resource "aws_instance" "selfoss-test" {
  ami                         = "ami-1c221e76"
  instance_type               = "t2.micro"
  subnet_id                   = "subnet-3832b84e"
  security_groups             = ["${aws_security_group.selfoss-test.id}"]
  key_name                    = "jeffhallyburton-east-1"

  provisioner "remote-exec" {
    connection {
      user         = ""
      agent        = true
      
    }

    inline = [
      "echo selfoss-test",
      ]
  }

}

resource "aws_eip" "selfoss-test_ip" {
  instance = "${aws_instance.selfoss-test.id}"
  vpc      = true
}

output "public_ip" {
  value = "${aws_eip.selfoss-test_ip.public_ip}"
}

output "private_ip" {
  value = "${aws_instance.selfoss-test.private_ip}"
}
