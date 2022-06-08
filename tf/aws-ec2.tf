module "argus-prod" {
  source = "./aws-ec2-argus"

  environment             = "prod"
  vpc_id                  = data.aws_vpc.default.id
  key_name                = "argus"
  whitelisted_cidr_blocks = local.whitelisted_cidr_blocks
}
