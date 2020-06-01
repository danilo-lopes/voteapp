import os
import MySQLdb


def getRedis():
    try:
        connRedis = Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            socket_timeout=5,
            decode_responses=True
        )

        return connRedis

    except Exception as erro:
        return f'Unable to connect to redis: {erro}'


def getMysql():
    try:
        coonMysql = MySQLdb.connect(
            host=os.getenv('MYSQL_HOST'),
            port=3306,
            user=os.getenv('MYSQL_USER'),
            passwd=os.getenv('MYSQL_PASSWORD')
        )

        return coonMysql

    except Exception as erro:
        return f'Unable to connect to mysql. {erro}'


def getVotes():

    daovotes = daoVotes()

    daovotes.getVotesFromRedis()
