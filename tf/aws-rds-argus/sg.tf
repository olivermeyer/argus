resource "aws_security_group" "this" {
  name   = local.common_resource_name
  vpc_id = var.vpc_id

  tags = {
    Name = local.common_resource_name
  }
}

resource "aws_security_group_rule" "allow-ingress-from-ec2-argus-sg" {
  for_each = var.ingress_sg_ids

  security_group_id        = aws_security_group.this.id
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = each.key
  description              = each.value
}

resource "aws_security_group_rule" "allow-ingress-from-my-ip" {
  security_group_id = aws_security_group.this.id
  type              = "ingress"
  from_port         = 5432
  to_port           = 5432
  protocol          = "tcp"
  cidr_blocks       = ["185.107.13.13/32"]
  description       = "allow-my-ip"
}
