terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "perso"
  region  = "eu-west-1"
}

resource "aws_instance" "argus" {
  ami           = "ami-0d1bf5b68307103c2"
  instance_type = "t2.micro"

  tags = {
    Name = "Argus"
  }
}
