module "aws-rds-argus-prod" {
  source = "./aws-rds-argus"

  environment  = "prod"
  rds_password = var.rds_password
  vpc_id       = data.aws_vpc.default.id
  ingress_sg_ids = {
    (module.argus-prod-2.sg_id) = "argus-prod-2"
  }
}
