resource "aws_security_group" "{{ name }}" {
  name_prefix   = "{{ prefix }}"
  description   = "{{ description }}"
  {% for port in ports %}
  ingress {
    from_port   = "{{ port }}"
    to_port     = "{{ port }}"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  {% endfor %}
  egress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = "${var.aws_vpc}"
}

