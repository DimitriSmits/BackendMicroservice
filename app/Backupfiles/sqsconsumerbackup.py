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




# import boto3
# import json
# import time

# class SQSConsumer:
#     def __init__(self, queue_url):
#         self.sqs = boto3.client('sqs',
#                                 endpoint_url='http://localhost:4566',
#                                 region_name='us-east-1',
#                                 aws_access_key_id='test',
#                                 aws_secret_access_key='test')
#         self.queue_url = queue_url

#     def consume(self, wait_time=20):
#         while True:
#             response = self.sqs.receive_message(QueueUrl=self.queue_url,
#                                                 WaitTimeSeconds=wait_time,
#                                                 MaxNumberOfMessages=1)
#             if 'Messages' in response:
#                 message = response['Messages'][0]
#                 body = message['Body']
#                 receipt_handle = message['ReceiptHandle']
#                 try:
#                     # Do something with the message body
#                     print(json.loads(body))
#                 except Exception as e:
#                     # Handle the exception as appropriate
#                     print(f'Error processing message: {str(e)}')
#                     self.sqs.change_message_visibility(QueueUrl=self.queue_url,
#                                                         ReceiptHandle=receipt_handle,
#                                                         VisibilityTimeout=0)
#                 else:
#                     # Delete the message from the queue
#                     self.sqs.delete_message(QueueUrl=self.queue_url,
#                                             ReceiptHandle=receipt_handle)
#             else:
#                 time.sleep(1)
