from dataBases import getSqsConnection
import json


class QueueService:

    def checkVotingSqsQueueHealth(self):
        sqs = getSqsConnection()

        getQueueUrl = sqs.get_queue_url(QueueName='voting')

        getMetadata = getQueueUrl['ResponseMetadata']

        queueStatusCode = getMetadata['HTTPStatusCode']

        return queueStatusCode

    def checkIfMessageIsValid(self, message):
        userMessage = json.loads(message)

        try:
            if userMessage['userID'] and userMessage['vote']:
                return 200

        except Exception as erro:
            return erro

    def sendMessage(self, message):
        data = message

        try:
            sqs = getSqsConnection()

            queueUrl = sqs.get_queue_url(QueueName='voting')['QueueUrl']

            sqs.send_message(
                QueueUrl=queueUrl,
                DelaySeconds=1,
                MessageBody=data
            )

            return 200

        except Exception as erro:
            return erro
