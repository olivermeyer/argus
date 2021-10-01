module "argus-prod-2" {
  source = "./aws-ec2-argus"

  environment = "prod-2"
  vpc_id      = data.aws_vpc.default.id
  key_name    = "argus"
}
