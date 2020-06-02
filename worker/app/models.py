import json
from dao import *


class Message:
    def __init__(self, body, messageID, receiptHandle):
        self.body = body
        self.messageID = messageID
        self.receiptHandle = receiptHandle


class QueueService:
    def __init__(self, sqsConnection):
        self.__sqsConnection = sqsConnection

    def getMessageFromSqs(self):
        sqsClient = self.__sqsConnection
        queueUrl = sqsClient.get_queue_by_name(QueueName='voting')

        sqsGetMessage = queueUrl.receive_messages(
            MaxNumberOfMessages=1,
            VisibilityTimeout=0,
            WaitTimeSeconds=20,
            MessageAttributeNames=['All']
        )

        data = sqsGetMessage

        return data

    def deleMessagesFromSqsQueue(self, message):
        sqsClient = self.__sqsConnection
        queueUrl = sqsClient.get_queue_by_name(QueueName='voting')

        queueUrl.delete_messages(
            Entries=[
                {
                    'Id': message.messageID,
                    'ReceiptHandle': message.receiptHandle
                },
            ]
        )


class MessageRepository:

    def storeMessageIntoDatabase(self, message):
        passMassageToJson = message.body

        MessagePassedToJson = json.loads(passMassageToJson)

        daoVote = VotingDao()

        daoVote.registerVote(MessagePassedToJson['userID'], MessagePassedToJson['vote'])
