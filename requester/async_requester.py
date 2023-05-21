"""
Implement an Async Requester
"""
import boto3
from redis import Redis

import logging

logger = logging.getLogger(__name__)


class AsyncRequester:
    """

    """

    def __init__(self, requester_identifier: str, queue_url: str) -> None:
        self.requester_identifier = requester_identifier
        self.queue_url = queue_url

    def send_request_and_wait(self, message: str):
        """
        Send the message to the Requests Queue and waits for the response in an
        pub/sub topic

        Args:
            message: the message
        """
        sqs_client = boto3.client('sqs')
        redis = Redis(host='localhost', port=6379)
        subscriber = redis.pubsub()

        message = sqs_client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message,
            MessageGroupId='default'
        )

        message_id = message['MessageId']

        logger.info('Sent message %s', message_id)

        subscriber.subscribe(message_id)

        # First call will always return a subscription messsage; ignore it
        response = subscriber.get_message(timeout=60)
        logger.info('First response: %s', response)
        response = subscriber.get_message(timeout=60)

        if response is None:
            raise Exception('Timeout while waiting for the response')

        print(response)
