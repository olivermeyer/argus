resource "aws_iam_instance_profile" "argus" {
  name = "argus"
  role = aws_iam_role.argus.name
}

resource "aws_iam_role" "argus" {
  name = "argus"
  assume_role_policy = data.aws_iam_policy_document.argus.json
}

data "aws_iam_policy_document" "argus" {
  version = "2012-10-17"

  statement {
    effect = "Allow"
    principals {
      identifiers = ["ec2.amazonaws.com"]
      type = "Service"
    }
    actions = [
      "sts:AssumeRole"
    ]
  }
}

resource "aws_iam_role_policy" "inline" {
  role = aws_iam_role.argus.id
  policy = data.aws_iam_policy_document.inline.json
}

data "aws_iam_policy_document" "inline" {
  version = "2012-10-17"

  statement {
    effect = "Allow"
    resources = ["*"]
    actions = [
      "ecr:*"
    ]
  }
}
