resource "aws_security_group" "{{ name }}" {
  name_prefix   = "{{ prefix }}"
  description   = "{{ description }}"
  {% if services is mapping %} 
    {% for service in services.itervalues() %} 
  ingress {
    from_port   = "{{ service['port'] }}"
    to_port     = "{{ service['port'] }}"
    protocol    = "{{ service['protocol'] }}"
    cidr_blocks = ["{{ service['range'] }}"]
  }
    {% endfor %}
  {% else %}     
    {% for service in services %}
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

