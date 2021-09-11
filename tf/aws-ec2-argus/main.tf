resource "aws_instance" "this" {
  ami                  = "ami-0d1bf5b68307103c2"
  instance_type        = "t2.micro"
  security_groups      = [aws_security_group.this.name]
  iam_instance_profile = aws_iam_instance_profile.this.name
  user_data            = file("${path.module}/user-data.bash")

  tags = {
    Name = local.common_resource_name
  }
}
