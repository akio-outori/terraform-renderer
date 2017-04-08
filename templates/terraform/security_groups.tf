{% for security_group in security_groups -%}
resource "aws_security_group" "{{ security_group['prefix'] }}" {
  {% if security_group['prefix'] is defined -%}
  name_prefix   = "{{ security_group['prefix'] }}"
  {% else -%}
  name          = "{{ security_group['name'] }}"
  {% endif -%}
  description   = "{{ security_group['description'] }}"
  {% if security_group['services'] is mapping -%} 
    {% for service in security_group['services'].itervalues() -%} 
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
  {% endif -%}
  egress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = "{{ security_group['vpc'] }}"
}
{% endfor -%}
