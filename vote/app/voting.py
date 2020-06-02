import boto3
import os
from flask import Flask

app = Flask(__name__)


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


from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
