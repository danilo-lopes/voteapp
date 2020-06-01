import os
import MySQLdb

coon = MySQLdb.connect(
    user=os.getenv('MYSQL_USER'),
    passwd=os.getenv('MYSQL_PASSWORD'),
    host=os.getenv('MYSQL_HOST'),
    port=3306
)

cursor = coon.cursor()

databaseCreation = '''SET NAMES utf8;
    CREATE DATABASE `voteapp` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
'''

cursor.execute(databaseCreation)

createTableUser = '''use `voteapp`;
    CREATE TABLE `user` (
        `id` varchar(40) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;
'''

cursor.execute(createTableUser)

createTableVote = '''use `voteapp`;
        CREATE TABLE `vote` (
            `voterid` varchar(40) COLLATE utf8_bin NOT NULL,
            `vote` varchar(10) COLLATE utf8_bin NOT NULL,
            PRIMARY KEY (`voterid`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
'''

cursor.execute(createTableVote)

cursor.close()
coon.commit()
coon.close()
