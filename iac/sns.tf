resource "aws_sns_topic" "my_topic" {
  name = "wiz-githubapp-action"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.my_topic.arn
  protocol  = "email"
  endpoint  = "elitegoblinrb@gmail.com"
}

output "sns_topic_arn" {
  value = aws_sns_topic.my_topic.arn
}