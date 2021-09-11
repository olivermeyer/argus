module "argus-prod-1" {
  source = "./aws-ec2-argus"

  environment = "prod-1"
  vpc_id      = data.aws_vpc.default.id
}
