variable "environment" {
  type = string
}

variable "rds_password" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "ingress_sg_ids" {
  type    = map(string)
  default = {}
}

variable "whitelisted_cidr_blocks" {
  type    = map(string)
  default = {}
}
