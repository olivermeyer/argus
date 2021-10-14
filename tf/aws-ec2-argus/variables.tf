variable "environment" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "key_name" {
  type    = string
  default = ""
}

variable "whitelisted_cidr_blocks" {
  type    = map(string)
  default = {}
}
