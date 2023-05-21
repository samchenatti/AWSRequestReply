import uuid
import logging
import os

QUEUE_URL = os.environ.get('QUEUE_URL')
if QUEUE_URL is None:
    raise ValueError('You need to set QUEUE_URL')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

if __name__ == '__main__':
    from async_requester import AsyncRequester

    async_requester = AsyncRequester(
        requester_identifier="requestes",
        queue_url=QUEUE_URL
    )

    async_requester.send_request_and_wait(message=f"test {uuid.uuid4()}")
