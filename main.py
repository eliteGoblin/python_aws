import boto3
import time
import json

from icecream import ic


REGION = 'ap-southeast-2'
AWS_ACCOUNT_ID = '555238755245'
SQS_QUEUE_NAME = 'wiz-githubapp-subscriber'

queue_url = f"https://sqs.{REGION}.amazonaws.com/{AWS_ACCOUNT_ID}/{SQS_QUEUE_NAME}"

# Initialize a session using Amazon SQS
sqs = boto3.client('sqs')

sns = boto3.client('sns')
sns_topic_arn = f"arn:aws:sns:{REGION}:{AWS_ACCOUNT_ID}:wiz-githubapp-action"

while True:  # Endless loop
    ic(f"Checking for messages in {queue_url}")
    # Receive message from SQS queue with long polling
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        WaitTimeSeconds=20  # Long polling for 20 seconds
    )

    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']

        # Print out the message body
        print(f"Received message: {message['Body']}")

        # Add field to the message
        msg_json = json.loads(message['Body'])
        msg_json['processed'] = "by fsun"

        # Publish to SNS topic
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=json.dumps(msg_json)
        )

        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
    else:
        print('No messages in queue. Waiting...')

    time.sleep(1)  # Sleep for 1 second before the next iteration
