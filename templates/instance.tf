resource "aws_instance" "{{ instance_name }}" {
  ami             = "${var.ami}"
  instance_type   = "{{ instance_type }}"
  subnet_id       = "${var.aws_subnet}"
  security_groups = ["${aws_security_group.{{ instance_name }}.id}"]
  key_name        = "${var.aws_keypair}"

  provisioner "remote-exec" {
    connection {
      user        = "${var.aws_user}"
      agent       = true
      private_key = "${file("~/.ssh/${var.aws_keypair}")}"
    }

    inline = [
      "sudo echo {{ instance_name }}"
    ]
  }

}

resource "aws_eip" "{{ instance_name }}_ip" {
  instance = "${aws_instance.{{ instance_name }}.id}"
}

output "ip" {
  value = "${aws_eip.{{ instance_name }}_ip.public_ip}"
}
