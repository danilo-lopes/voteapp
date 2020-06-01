import json
import time
import sys
from voting import getSqsConnection


def checkSizeQueue(sqsClient, queueUrl):
    sizeOfQueue = sqsClient.get_queue_attributes(
        QueueUrl=queueUrl,
        AttributeNames=['ApproximateNumberOfMessages']
    )['Attributes']['ApproximateNumberOfMessages']

    return sizeOfQueue


def getMessage(sqsClient, queueUrl):
    queueSize = checkSizeQueue(sqsClient, queueUrl)

    if queueSize != '0':
        sqsGetMessageQuery = sqsClient.receive_message(
            QueueUrl=queueUrl,
            MaxNumberOfMessages=1,
            VisibilityTimeout=0,
            WaitTimeSeconds=0,
            MessageAttributeNames=['All']
        )

        ReturnOfSqsGetMessage = sqsGetMessageQuery['Messages'][0]

        message = json.loads(ReturnOfSqsGetMessage['Body'])

        receipt_handle = ReturnOfSqsGetMessage['ReceiptHandle']

        data = json.dumps(
            {
                'userID': message["userID"],
                'vote': message["vote"],
                'receiptHandleOfMessage': receipt_handle
            }
        )

        return data

    else:
        data = json.dumps(
            {
                'userID': None
            }
        )

        return data


def storeMassageIntoMysql(sqsClient, queueUrl):
    while True:
        message = json.loads(getMessage(sqsClient, queueUrl))

        if not message['userID']:
            sys.exit('No more messages to process')

        print(
            f'userID: {message["userID"]} - vote: {message["vote"]} - receiptHandle: {message["receiptHandleOfMessage"]}')

        print(f'The massage of userID: {message["userID"]} will be stored and after deleted in 5 secound..')

        time.sleep(5)
        sqsClient.delete_message(
            QueueUrl=queueUrl,
            ReceiptHandle=message['receiptHandleOfMessage']
        )


sqsClient = getSqsConnection()
testQueueUrl = sqsClient.get_queue_url(QueueName='test')['QueueUrl']

print(
    storeMassageIntoMysql(sqsClient, testQueueUrl)
)
