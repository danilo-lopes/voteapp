from dataBases import GetMysqlConnection


SQL_GET_COCA_VOTES = 'SELECT COUNT(vote) from votes where vote="coca"'
SQL_GET_PEPSI_VOTES = 'SELECT COUNT(vote) from votes where vote="pepsi"'


class GetvotesFromSql:

    def getCocaVotes(self):
        mysqlConnection = GetMysqlConnection()
        cursor = mysqlConnection.cursor()

        cursor.execute(SQL_GET_COCA_VOTES)

        data = cursor.fetchone()

        return traduzVotes(data)

    def getPepsiVotes(self):
        mysqlConnection = GetMysqlConnection()
        cursor = mysqlConnection.cursor()

        cursor.execute(SQL_GET_PEPSI_VOTES)

        data = cursor.fetchone()

        return traduzVotes(data)


def traduzVotes(tupla):
    return tupla[0] if tupla else None
