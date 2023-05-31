import asyncio
import boto3
import json
from fastapi import Depends
from sqlalchemy.orm import Session
from route_dependencies import get_db
from exceptions import InvalidQueueUrlError
from services import EventService
from schemas import RequestEvent
from schemas import EventSchema
from services import BatchService

class SQSConsumer:

    def __init__(self, queue_url):
        try:
            self.sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')
            self.queue_url = queue_url
            self.db = get_db()
        except Exception as e:
            raise InvalidQueueUrlError(f"Invalid queue URL {queue_url}: {str(e)}")
    async def process_message(self, message):
        # Delete the message from the queue
        self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message['ReceiptHandle'])

    async def consume_messages(self):
        events = []

        while True:
            try:
                response = self.sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=1)
            except Exception as e:
                print(f"Error: {str(e)}. Retrying in 5 minutes.")
                await asyncio.sleep(300)  # retry in 5 minutes
                continue
            if 'Messages' not in response:
                print(f"No new messages, polling again in 1 minute")
                await asyncio.sleep(60)
                continue

            # for message in response['Messages']:
            #     print(f"Found a message")
            #     message = response['Messages'][0]
            #     body = message['Body']
            #     receipt_handle = message['ReceiptHandle']
            #     try:
            #         json_obj = json.loads(body)
            #         request_event = RequestEvent(**json_obj)
            #         self.db = next(get_db())
            #         EventService.create_event(self.db, event=request_event.parameter)
            for message in response['Messages']:
                print(f"Found a message")
                message = response['Messages'][0]
                body = message['Body']
                receipt_handle = message['ReceiptHandle']
                try:
                    json_obj = json.loads(body)
                    request_event = RequestEvent(**json_obj)
                    events.append(request_event.parameter)
                    #If list of events is higher than 100 then send it to the db
                    if len(events) >= 1:
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
                    self.sqs.change_message_visibility(QueueUrl=self.queue_url,
                                                        ReceiptHandle=receipt_handle,
                                                        VisibilityTimeout=0)
                #Nieuw
                #
                # if events and len(events) < 100:
                #     print(f"Hij was onder de 100 gaat nu processen")
                #     EventService.process_events(self.db, events)
                #     events = []  # Clear the event batch
                try:
                    await self.process_message(message)
                except Exception as e:
                    print('Error processing message:', str(e))

    async def cleanup(self):
        self.db.close()
                

    async def run(self):
        await self.consume_messages()
