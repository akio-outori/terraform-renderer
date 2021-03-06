resource "aws_instance" "bettermeans" {
  ami             = "${var.ami}"
  instance_type   = "${var.instance_type}"
  subnet_id       = "${var.aws_subnet}"
  security_groups = ["${aws_security_group.bettermeans.id}"]
  key_name        = "${var.aws_keypair}"

  provisioner "remote-exec" {
    connection {
      user        = "${var.aws_user}"
      agent       = true
      private_key = "${file("~/.ssh/${var.aws_keypair}")}"
    }

    script = "bettermeans.sh"
    }
}

resource "aws_eip" "bettermeans-ip" {
  instance = "${aws_instance.bettermeans.id}"
}

output "ip" {
  value = "${aws_eip.bettermeans-ip.public_ip}"
}