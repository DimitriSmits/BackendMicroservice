import boto3
import asyncio
from botocore.exceptions import NoCredentialsError

def receive_message(queue_url):
    # Create a boto3 client for SQS
    sqs = boto3.client('sqs')
    
    # Receive messages from the queue
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )
    except NoCredentialsError:
        # Handle the case where AWS credentials are missing or invalid
        print('Error: AWS credentials are missing or invalid')
    else:
        # Return the received message (if any)
        messages = response.get('Messages')
        if messages:
            message = messages[0]
            receipt_handle = message['ReceiptHandle']
            message_body = message['Body']
            return message_body, receipt_handle
        else:
            return None, None
        
async def process_messages_endpoint():
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'
    
    while True:
        # Receive a message from the queue
        message, receipt_handle = receive_message(queue_url)
        
        if message is None:
            # No messages in the queue, wait and try again
            await asyncio.sleep(10)
            continue
        
        try:
            # Process the message
            # ...
            
            # Delete the message from the queue
            sqs = boto3.client('sqs')
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
        except:
            # Handle any errors that occur while processing the message
            pass