from dataBases import sqsConnection


class ApiSqsService:

    def checkVotingSqsQueueHealth(self):
        sqs = sqsConnection()

        try:
            getQueueUrl = sqs.get_queue_by_name(QueueName='voting')

            getMetadata = getQueueUrl.attributes['QueueArn']

            if getMetadata:
                return 200

        except Exception as erro:
            return erro
