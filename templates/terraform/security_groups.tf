resource "aws_security_group" "{{ instance['name'] }}" {
  name_prefix   = "{{ security_group['prefix'] }}"
  description   = "{{ security_group['description'] }}"
  {% if security_group['services'] is mapping %} 
    {% for service in security_group['services'].itervalues() %} 
  ingress {
    from_port   = "{{ service['port'] }}"
    to_port     = "{{ service['port'] }}"
    protocol    = "{{ service['protocol'] }}"
    cidr_blocks = ["{{ service['range'] }}"]
  }
    {% endfor %}
  {% else %}     
    {% for service in security_group['services'] %}
  ingress {
    from_port   = "{{ service }}"
    to_port     = "{{ service }}"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
    {% endfor %}
  {% endif %}
  egress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = "${var.aws_vpc}"
}

