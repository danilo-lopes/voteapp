import boto3
import os


def getSqsConnection():
    try:
        sqsClient = boto3.client(
            'sqs',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
            region_name=os.getenv('AWS_REGION')
        )

        return sqsClient

    except Exception as erro:
        return f'Connection erro: {erro}'
