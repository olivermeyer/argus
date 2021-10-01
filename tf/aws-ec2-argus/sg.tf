resource "aws_security_group" "this" {
  name   = local.common_resource_name
  vpc_id = var.vpc_id

  tags = {
    Name = "Argus"
  }
}

resource "aws_security_group_rule" "allow-ingress-from-console" {
  security_group_id = aws_security_group.this.id
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["18.202.216.48/29"]
  description       = "allow-ec2-instance-connect"
}

resource "aws_security_group_rule" "allow-ingress-from-my-ip" {
  security_group_id = aws_security_group.this.id
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["185.107.13.13/32"]
  description       = "allow-my-ip"
}

resource "aws_security_group_rule" "allow-egress" {
  security_group_id = aws_security_group.this.id
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = ["::/0"]
}
