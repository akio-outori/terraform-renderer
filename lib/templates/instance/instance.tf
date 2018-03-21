resource "aws_instance" "{{ variables['name'] }}" {
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

    {% if variables['configuration']['script'] -%}
    script = "{{ variables['configuration']['script'] }}"
    {% endif -%}
  }
}

resource "aws_eip" "{{ variables['name'] }}-ip" {
  instance = "${aws_instance.{{ variables['name'] }}.id}"
}

output "ip" {
  value = "${aws_eip.{{ variables['name'] }}-ip.public_ip}"
}
