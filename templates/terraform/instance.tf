resource "aws_instance" "{{ instance['name'] }}" {
  ami             = "${var.ami}"
  instance_type   = "{{ instance['type'] }}"
  subnet_id       = "${var.aws_subnet}"
  security_groups = ["${aws_security_group.{{ instance['name'] }}.id}"]
  {% if instance['associate_public_ip'] == "true" -%}
  associate_public_ip_address = true
  {% endif -%}
  key_name        = "${var.aws_keypair}"

  provisioner "file" {
    connection {
      user         = "${var.aws_user}"
      agent        = true
      {% if instance['bastion_host'] -%}
      bastion_host = "{{ instance['bastion_host'] }}"
      bastion_user = "${var.aws_user}"
      {% endif %}
    }
   
    source      = "files/{{ instance['config_script']}}"
    destination = "~/{{ instance['config_script'] }}"
  }
  
  provisioner "remote-exec" {
    connection {
      user         = "${var.aws_user}"
      agent        = true
      {% if instance['bastion_host'] -%}
      bastion_host = "{{ instance['bastion_host'] }}"
      bastion_user = "${var.aws_user}"
      {% endif %}
    }

    inline = [
      "chmod +x ~/{{ instance['config_script'] }}",
      "sudo ~/{{ instance['config_script'] }}"
    ]
  }

}

resource "aws_eip" "{{ instance['name'] }}_ip" {
  instance = "${aws_instance.{{ instance['name'] }}.id}"
  vpc      = true
}

output "public_ip" {
  value = "${aws_eip.{{ instance['name'] }}_ip.public_ip}"
}

output "private_ip" {
  value = "${aws_instance.{{ instance['name'] }}.private_ip}"
}

