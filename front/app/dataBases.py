import os
import MySQLdb


def GetMysqlConnection():
    try:
        mysqlClient = MySQLdb.connect(
            host=os.getenv('MYSQL_HOST'),
            port=3306,
            user=os.getenv('MYSQL_USER'),
            db=os.getenv('MYSQL_DB'),
            passwd=os.getenv('MYSQL_PASSWORD')
        )

        return mysqlClient

    except Exception as erro:
        return f'Connection erro. {erro}'
