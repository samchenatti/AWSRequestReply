import boto3
from redis import Redis
import time
import logging
import os

QUEUE_URL = os.environ.get('QUEUE_URL')
if QUEUE_URL is None:
    raise ValueError('You need to set QUEUE_URL')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    sqs_client = boto3.client('sqs')
    redis = Redis(host='localhost', port=6379)

    while True:
        messages = sqs_client.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5
        )
        print(messages.keys())
        if 'Messages' not in messages:
            logger.info('No messages received')
            continue

        logger.info('Received %d messages', len(messages['Messages']))

        for message in messages['Messages']:
            time.sleep(10)

            body = message['Body']
            message_id = message['MessageId']

            logger.info('Processing message %s', message_id)

            redis.publish(
                message_id,
                f'Hello, {message_id} owner; echoing: ' + body
            )

            sqs_client.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )
