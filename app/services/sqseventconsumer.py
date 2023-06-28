import asyncio
import boto3
import json
import os
from fastapi import Depends
from sqlalchemy.orm import Session
from route_dependencies import get_db
from exceptions import InvalidQueueUrlError
from services import EventService
from services import UserService
from schemas import RequestEvent
from schemas import EventSchema
from schemas import UserSchema
from services import BatchService
from dotenv import load_dotenv

load_dotenv()


class SQSEventConsumer:

    def __init__(self):
        try:
            self.sqs = boto3.client('sqs', region_name=os.getenv('REGION_NAME'),
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                endpoint_url=os.getenv('ENDPOINT_URL'))
            self.queue_url = os.getenv('QUEUE_URL')
            self.db = get_db()
        except Exception as exception:
            raise InvalidQueueUrlError(f"Invalid queue URL {os.getenv('QUEUE_URL')}: {str(exception)}")
    async def process_message(self, message, queueurl):
        # Delete the message from the queue
        self.sqs.delete_message(QueueUrl=queueurl, ReceiptHandle=message['ReceiptHandle'])

    async def consume_messages(self):
        events = []
        # Get delay timers from .env, if not found than standard is 300s/5 minutes and batch size
        retry_delay = int(os.getenv('RETRY_DELAY', 300))
        consume_delay = int(os.getenv('CONSUME_DELAY', 300))
        batch_size = int(os.getenv('BATCH_SIZE', 100))

        while True:
            try:
                response = self.sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=1)
            except Exception as e:
                print(f"Error: {str(e)}. Retrying in 5 minutes.")
                await asyncio.sleep(retry_delay)  # retry in 5 minutes
                continue
            if 'Messages' not in response:
                print(f"No new messages, polling again in 1 minute")
                await asyncio.sleep(consume_delay)
                continue

            for message in response['Messages']:
                print("Found a message")
                body = message['Body']
                receipt_handle = message['ReceiptHandle']
                try:
                    json_obj = json.loads(body)
                    if 'events' in json_obj:
                        for event in json_obj['events']:
                            request_event = RequestEvent(**event)
                            events.append(request_event.parameter)
                    else:
                        request_event = RequestEvent(**json_obj)
                        events.append(request_event.parameter)
                    # If the list of events is higher than the batch size, send it to the database
                    if len(events) >= batch_size:
                        self.db = next(get_db())
                        batch_id = BatchService.create_batch(self.db)
                        updated_events = []
                        for event in events:
                            event.batch_id = batch_id
                            updated_events.append(event)
                        events = updated_events
                        EventService.process_events(self.db, events)
                        events = []

                except Exception as e:
                    # Handle the exception as appropriate
                    print(f'Error processing message: {str(e)}')
                    self.sqs.change_message_visibility(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=receipt_handle,
                        VisibilityTimeout=0
                    )
                try:
                    await self.process_message(message, self.queue_url)
                except Exception as e:
                    print('Error processing message:', str(e))

    async def cleanup(self):
        self.db.close()
                

    async def run(self):
        await self.consume_messages()