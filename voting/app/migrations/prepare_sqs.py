import boto3
import os


def createQueue():
    sqsClient = boto3.client(
        'sqs',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    if checkIfAlreadyExists() == 'voting':
        return 'voting'

    else:
        result = sqsClient.create_queue(
            QueueName='voting'
        )

        return result['ResponseMetadata']['HTTPStatusCode']


def checkIfAlreadyExists():
    try:
        sqsClient = boto3.client(
            'sqs',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
            region_name=os.getenv('AWS_REGION')
        )

        votingQueueUrl = sqsClient.get_queue_url(
            QueueName='voting'
        )['QueueUrl']

        return votingQueueUrl.split('/')[-1]

    except:
        return None
