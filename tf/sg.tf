data "aws_vpc" "default" {
  id = "vpc-b65760d0"
}

resource "aws_security_group" "argus" {
  name   = "argus"
  vpc_id = data.aws_vpc.default.id

  tags = {
    Name = "Argus"
  }
}

resource "aws_security_group_rule" "allow-ingress-from-console" {
  security_group_id = aws_security_group.argus.id
  type = "ingress"
  from_port = 22
  to_port = 22
  protocol = "tcp"
  cidr_blocks = ["18.202.216.48/29"]
}

resource "aws_security_group_rule" "allow-egress" {
  security_group_id = aws_security_group.argus.id
  type = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = ["::/0"]
}
