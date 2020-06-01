import os
import MySQLdb

coon = MySQLdb.connect(
    user=os.getenv('MYSQL_USER'),
    passwd=os.getenv('MYSQL_PASSWORD'),
    host=os.getenv('MYSQL_HOST'),
    port=3306
)

cursor = coon.cursor()

createDatabase = '''SET NAMES utf8;
    CREATE DATABASE `voteapp` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
'''

cursor.execute(createDatabase)

createTableVoting = '''use `voteapp`;
    CREATE TABLE `voting` (
        `id` varchar(40) NOT NULL,
        `vote` varchar(40) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;
'''

cursor.execute(createTableVoting)

cursor.close()
coon.commit()
coon.close()
