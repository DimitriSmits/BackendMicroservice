import asyncio
import boto3
import json
from fastapi import Depends
from sqlalchemy.orm import Session
from route_dependencies import get_db
from services import EventService
from schemas import RequestEvent

class SQSConsumer:

    def __init__(self, queue_url):
        self.sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')
        self.queue_url = queue_url
        self.db = get_db()

    async def process_message(self, message):
        # Delete the message from the queue
        self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message['ReceiptHandle'])

    async def consume_messages(self):
        while True:
            response = self.sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=1)
            if 'Messages' not in response:
                await asyncio.sleep(1)
                continue

            for message in response['Messages']:
                message = response['Messages'][0]
                body = message['Body']
                receipt_handle = message['ReceiptHandle']
                try:
                    json_obj = json.loads(body)
                    request_event = RequestEvent(**json_obj)
                    self.db = next(get_db())
                    EventService.create_event(self.db, event=request_event.parameter)

                except Exception as e:
                    # Handle the exception as appropriate
                    print(f'Error processing message: {str(e)}')
                    self.sqs.change_message_visibility(QueueUrl=self.queue_url,
                                                        ReceiptHandle=receipt_handle,
                                                        VisibilityTimeout=0)
                #Nieuw
                try:
                    await self.process_message(message)
                except Exception as e:
                    print('Error processing message:', str(e))

    async def cleanup(self):
        self.db.close()
                

    async def run(self):
        await self.consume_messages()
