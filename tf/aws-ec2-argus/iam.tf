resource "aws_iam_instance_profile" "this" {
  name = local.common_resource_name
  role = aws_iam_role.this.name
}

resource "aws_iam_role" "this" {
  name               = local.common_resource_name
  assume_role_policy = data.aws_iam_policy_document.this.json
}
data "aws_iam_policy_document" "this" {
  version = "2012-10-17"

  statement {
    effect = "Allow"
    principals {
      identifiers = ["ec2.amazonaws.com"]
      type        = "Service"
    }
    actions = [
      "sts:AssumeRole"
    ]
  }
}

resource "aws_iam_role_policy" "inline" {
  role   = aws_iam_role.this.id
  policy = data.aws_iam_policy_document.inline.json
}

data "aws_iam_policy_document" "inline" {
  version = "2012-10-17"

  statement {
    effect    = "Allow"
    resources = ["*"]
    actions = [
      "ecr:*"
    ]
  }
}
