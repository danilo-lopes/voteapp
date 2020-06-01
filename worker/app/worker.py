import os
import boto3


def sqsConnection():
    sqsClient = None

    while not sqsClient:
        try:
            session = boto3.session.Session()
            sqsClient = session.resource(
                'sqs',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                region_name=os.getenv('AWS_REGION')
            )

            return sqsClient

        except:
            return None


# def mysqlConnection():
#     try:
#         coonMysql = MySQLdb.connect(
#             host=os.getenv('MYSQL_HOST'),
#             port=3306,
#             user=os.getenv('MYSQL_USER'),
#             passwd=os.getenv('MYSQL_PASSWORD')
#         )
#
#         return coonMysql
#
#     except Exception as erro:
#         return f'Connection erro. {erro}'
