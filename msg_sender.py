import boto3
import json

REGION = 'ap-southeast-2'
AWS_ACCOUNT_ID = '555238755245'
SQS_QUEUE_NAME = 'wiz-githubapp-subscriber'

queue_url = f"https://sqs.{REGION}.amazonaws.com/{AWS_ACCOUNT_ID}/{SQS_QUEUE_NAME}"

# Read the JSON content from the local file
with open('./data/hello.json', 'r') as file:
    message_body = json.load(file)

# Convert the Python dictionary back to JSON string
message_body_str = json.dumps(message_body)

# Initialize a session using Amazon SQS
sqs = boto3.client('sqs')

# Send message to SQS queue
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=message_body_str
)

print(f"Message sent with ID: {response['MessageId']}")
