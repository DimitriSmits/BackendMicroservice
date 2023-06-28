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


class SQSConsumer:

    def __init__(self):
        try:
            self.sqs = boto3.client('sqs', region_name=os.getenv('REGION_NAME'),
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                endpoint_url=os.getenv('ENDPOINT_URL'))
            # self.queue_url = os.getenv('QUEUE_URL')
            self.queue_url_2 = os.getenv('USERSQUEUE_URL')
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
        # batch_size = int(os.getenv('BATCH_SIZE', 100))

        # while True:
        #     try:
        #         response = self.sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=1)
        #     except Exception as e:
        #         print(f"Error: {str(e)}. Retrying in 5 minutes.")
        #         await asyncio.sleep(retry_delay)  # retry in 5 minutes
        #         continue
        #     if 'Messages' not in response:
        #         print(f"No new messages, polling again in 1 minute")
        #         await asyncio.sleep(consume_delay)
        #         continue

        #     for message in response['Messages']:
        #         print(f"Found a message")
        #         message = response['Messages'][0]
        #         body = message['Body']
        #         receipt_handle = message['ReceiptHandle']
        #         try:
        #             json_obj = json.loads(body)
        #             request_event = RequestEvent(**json_obj)
        #             events.append(request_event.parameter)
        #             # If the list of events is higher than the batch size, send it to the database
        #             if len(events) >= batch_size:
        #                 self.db = next(get_db())
        #                 batch_id = BatchService.create_batch(self.db)
        #                 updated_events = []
        #                 for event in events:
        #                     event.batch_id = batch_id
        #                     updated_events.append(event)
        #                 events = updated_events
        #                 EventService.process_events(self.db, events)
        #                 events = []

        #         except Exception as e:
        #             # Handle the exception as appropriate
        #             print(f'Error processing message: {str(e)}')
        #             self.sqs.change_message_visibility(
        #                 QueueUrl=self.queue_url,
        #                 ReceiptHandle=receipt_handle,
        #                 VisibilityTimeout=0
        #             )
        #         try:
        #             await self.process_message(message, self.queue_url)
        #         except Exception as e:
        #             print('Error processing message:', str(e))

        #     # Consume messages from the second queue
        #     response_2 = self.sqs.receive_message(QueueUrl=self.queue_url_2, MaxNumberOfMessages=1)
        #     if 'Messages' not in response_2:
        #         print(f"No new messages in Queue 2, polling again in 1 minute")
        #         await asyncio.sleep(consume_delay)
        #         continue

        #     for message in response_2['Messages']:
        #         # Process messages from the second queue
        #         body = message['Body']
        #         print(f"Message from Queue 2: {body}")

        #         data = json.loads(body)

        #         # Create a UserSchema instance using the deserialized data
        #         user_schema = UserSchema(**data['parameter'])

        #         self.db = next(get_db())
        #         UserService.create_user(self.db,user_schema)

        #         try:
        #             await self.process_message(message, self.queue_url_2)
        #         except Exception as e:
        #             print('Error processing message:', str(e))
        while True:
            try:
                response_2 = self.sqs.receive_message(QueueUrl=self.queue_url_2, MaxNumberOfMessages=1)
            except Exception as e:
                print(f"Error: {str(e)}. Retrying in 5 minutes.")
                await asyncio.sleep(retry_delay)  # retry in 5 minutes
                continue

            if 'Messages' in response_2:
                for message in response_2['Messages']:
                    # Process messages from the second queue
                    body = message['Body']
                    print(f"Message from Queue 2: {body}")

                    data = json.loads(body)

                    # Create a UserSchema instance using the deserialized data
                    user_schema = UserSchema(**data['parameter'])

                    self.db = next(get_db())
                    UserService.create_user(self.db, user_schema)

                    try:
                        await self.process_message(message, self.queue_url_2)
                    except Exception as e:
                        print('Error processing message:', str(e))
                continue

            # try:
            #     response = self.sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=1)
            # except Exception as e:
            #     print(f"Error: {str(e)}. Retrying in 5 minutes.")
            #     await asyncio.sleep(retry_delay)  # retry in 5 minutes
            #     continue

            # if 'Messages' not in response:
            #     print(f"No new messages in queue 1, polling again in 1 minute")
            #     await asyncio.sleep(consume_delay)
            #     continue

            # for message in response['Messages']:
            #     print(f"Found a message in queue 1")
            #     message = response['Messages'][0]
            #     body = message['Body']
            #     receipt_handle = message['ReceiptHandle']
            #     try:
            #         json_obj = json.loads(body)
            #         request_event = RequestEvent(**json_obj)
            #         events.append(request_event.parameter)
            #         # If the list of events is higher than the batch size, send it to the database
            #         if len(events) >= batch_size:
            #             self.db = next(get_db())
            #             batch_id = BatchService.create_batch(self.db)
            #             updated_events = []
            #             for event in events:
            #                 event.batch_id = batch_id
            #                 updated_events.append(event)
            #             events = updated_events
            #             EventService.process_events(self.db, events)
            #             events = []

            #     except Exception as e:
            #         # Handle the exception as appropriate
            #         print(f'Error processing message: {str(e)}')
            #         self.sqs.change_message_visibility(
            #             QueueUrl=self.queue_url,
            #             ReceiptHandle=receipt_handle,
            #             VisibilityTimeout=0
            #         )
            #     try:
            #         await self.process_message(message, self.queue_url)
            #     except Exception as e:
            #         print('Error processing message:', str(e))

            print(f"No new messages in Queue 2, polling again in 1 minute")
            await asyncio.sleep(consume_delay)


    async def cleanup(self):
        self.db.close()
                

    async def run(self):
        await self.consume_messages()
