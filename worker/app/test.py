import json
import time
from worker import sqsConnection


def checkSizeQueue(queue):
    sizeOfQueue = queue.attributes['ApproximateNumberOfMessages']

    return sizeOfQueue


def getMessage(queue):
    queueSize = checkSizeQueue(queue)

    if queueSize != '0':
        sqsGetMessageQuery = queue.receive_messages(
            MaxNumberOfMessages=1,
            VisibilityTimeout=0,
            WaitTimeSeconds=0,
            MessageAttributeNames=['All']
        )

        messageToDump = [message.body for message in sqsGetMessageQuery][0]
        messageIDToDump = [message.message_id for message in sqsGetMessageQuery][0]
        receiptHandleToDump = [message.receipt_handle for message in sqsGetMessageQuery][0]

        message = json.loads(messageToDump)
        messageID = str(messageIDToDump)
        receiptHandle = str(receiptHandleToDump)

        data = json.dumps(
            {
                'userID': message["userID"],
                'vote': message["vote"],
                'receiptHandle': receiptHandle,
                'messageID': messageID
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


def storeMassageIntoMysql(queue):
    while True:
        messageJson = getMessage(queue)

        time.sleep(2)

        message = json.loads(messageJson)

        if not message['userID']:
            continue

        print(
            f'userID: {message["userID"]} - vote: {message["vote"]} - receiptHandle: {message["receiptHandle"]}')

        print(f'The massage of userID: {message["userID"]} will be stored and after deleted in 5 secound..')

        time.sleep(5)
        queue.delete_messages(
            Entries=[
                {
                    'Id': message['messageID'],
                    'ReceiptHandle': message['receiptHandle']
                },
            ]
        )


sqsClient = sqsConnection()
votingQueueUrl = sqsClient.get_queue_by_name(QueueName='voting')

print(
    storeMassageIntoMysql(votingQueueUrl)
)
