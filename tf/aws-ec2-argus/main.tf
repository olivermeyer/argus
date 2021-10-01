resource "aws_instance" "this" {
  ami                  = "ami-0d1bf5b68307103c2"
  instance_type        = "t2.micro"
  security_groups      = [aws_security_group.this.name]
  iam_instance_profile = aws_iam_instance_profile.this.name
  user_data            = file("${path.module}/user-data.bash")
  key_name             = var.key_name

  tags = {
    Name = local.common_resource_name
  }

  lifecycle {
    ignore_changes = [user_data]
  }
}
