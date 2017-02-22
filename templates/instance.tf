resource "aws_instance" "{{ instance['name'] }}" {
  ami             = "${var.ami}"
  instance_type   = "{{ instance['type'] }}"
  subnet_id       = "${var.aws_subnet}"
  security_groups = ["${aws_security_group.{{ instance['name'] }}.id}"]
  key_name        = "${var.aws_keypair}"

  provisioner "remote-exec" {
    connection {
      user        = "${var.aws_user}"
      agent       = true
      private_key = "${file("~/.ssh/${var.aws_keypair}")}"
    }

    inline = [
      "sudo echo {{ instance['name'] }}"
    ]
  }

}

resource "aws_eip" "{{ instance['name'] }}_ip" {
  instance = "${aws_instance.{{ instance['name'] }}.id}"
}

output "ip" {
  value = "${aws_eip.{{ instance['name'] }}_ip.public_ip}"
}
