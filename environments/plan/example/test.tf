resource "aws_instance" "test" {
  ami                         = "ami-1c221e76"
  instance_type               = "t2.micro"
  subnet_id                   = "test"
  security_groups             = ["${aws_security_group.test.id}"]
  key_name                    = "test"

  provisioner "remote-exec" {
    connection {
      user         = "centos"
      agent        = true
      
    }

    inline = [
      "echo test",
      ]
  }

}

resource "aws_eip" "test_ip" {
  instance = "${aws_instance.test.id}"
  vpc      = true
}

output "public_ip" {
  value = "${aws_eip.test_ip.public_ip}"
}

output "private_ip" {
  value = "${aws_instance.test.private_ip}"
}
