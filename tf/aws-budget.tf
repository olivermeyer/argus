resource "aws_budgets_budget" "all-20-dollars-monthly" {
  name              = "all-20-dollars-monthly"
  budget_type       = "COST"
  limit_amount      = "20"
  limit_unit        = "USD"
  time_period_start = "2021-10-01_00:00"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["meyer.oliver93@gmail.com"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["meyer.oliver93@gmail.com"]
  }
}
