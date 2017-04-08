resource "aws_instance" "{{ instance['name'] }}" {
  ami                         = "{{ instance['ami'] }}"
  instance_type               = "{{ instance['type'] }}"
  subnet_id                   = "{{ random.choice(instance['subnet'].values()) }}"
  security_groups             = ["${aws_security_group.{{ instance['security_group'] }}.id}"]
  {% if instance['associate_public_ip'] == "true" -%}
  associate_public_ip_address = true
  {% endif -%}
  key_name                    = "{{ instance['keypair'] }}"

  {% for file in instance['config_files'] -%}
  provisioner "file" {
    connection {
      user         = "{{ instance['user'] }}"
      agent        = true
      {% if variables['bastion_host'] -%}
      bastion_host = "{{ variables['bastion_host'] }}"
      bastion_user = "{{ variables['bastion_user'] }}"
      {% endif %}
    }
   
    source      = "files/{{ file }}"
    destination = "{{ instance['config_dir'] }}/{{ os.path.basename(file) }}"
  }

  {% endfor -%}
  
  provisioner "remote-exec" {
    connection {
      user         = "{{ instance['user'] }}"
      agent        = true
      {% if variables['bastion_host'] -%}
      bastion_host = "{{ variables['bastion_host'] }}"
      bastion_user = "{{ variables['bastion_user'] }}"
      {% endif %}
    }

    inline = [
      "echo {{ instance['name'] }}",
      {% if instance['config_script'] -%}
      "chmod +x {{ instance['config_script'] }}",
      "sudo {{ instance['config_script'] }}"
      {% endif -%}
    ]
  }

}

resource "aws_eip" "{{ instance['name'] }}_ip" {
  instance = "${aws_instance.{{ instance['name'] }}.id}"
  vpc      = true
}

output "{{ instance['name'] }}_public_ip" {
  value = "${aws_eip.{{ instance['name'] }}_ip.public_ip}"
}

output "{{ instance['name'] }}_private_ip" {
  value = "${aws_instance.{{ instance['name'] }}.private_ip}"
}

