resource "aws_db_instance" "this" {
  identifier             = "argus-${var.environment}"
  name                   = "argus"
  instance_class         = "db.t3.micro"
  engine                 = "postgres"
  engine_version         = "13.4"
  username               = "argus"
  password               = var.rds_password
  vpc_security_group_ids = [aws_security_group.this.id]
  allocated_storage      = 10
  skip_final_snapshot    = true
  publicly_accessible    = true
}
