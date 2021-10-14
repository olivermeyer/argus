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

resource "aws_security_group_rule" "allow-ingress-from-cidr_blocks" {
  for_each = var.whitelisted_cidr_blocks

  security_group_id = aws_security_group.this.id
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = [each.key]
  description       = "allow-${each.value}"
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
