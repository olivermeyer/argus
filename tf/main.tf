resource "aws_instance" "argus" {
  ami           = "ami-0d1bf5b68307103c2"
  instance_type = "t2.micro"
  security_groups = [aws_security_group.argus.name]
  iam_instance_profile = aws_iam_instance_profile.argus.name
  user_data = file("${path.module}/user-data.bash")

  tags = {
    Name = "Argus"
  }
}
