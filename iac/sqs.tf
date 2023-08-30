provider "aws" {
  region = "ap-southeast-2"  # Replace with your desired region
  profile = "elitegoblinrb"
}

resource "aws_sqs_queue" "wiz_githubapp_subscriber" {
  name = "wiz-githubapp-subscriber"
  delay_seconds = 0
  max_message_size = 262144
  message_retention_seconds = 345600
  receive_wait_time_seconds = 0
  visibility_timeout_seconds = 120

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.wiz_githubapp_subscriber_dlq.arn
    maxReceiveCount     = 5
  })

  # Enable server-side encryption
  kms_master_key_id = "alias/aws/sqs"
  kms_data_key_reuse_period_seconds = 300
}

resource "aws_sqs_queue" "wiz_githubapp_subscriber_dlq" {
  name = "wiz-githubapp-subscriber-dlq"
}