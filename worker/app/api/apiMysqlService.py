from dataBases import GetMysqlConnection

SQL_GET_DATABASE = 'SELECT SCHEMA_NAME from INFORMATION_SCHEMA.SCHEMATA where SCHEMA_NAME = "voteapp"'
SQL_GET_TABLE = 'SELECT TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_NAME = "votes"'


class ApiMysqlService:

    def checkDatabaseHealth(self):
        mysqlConnection = GetMysqlConnection()
        cursor = mysqlConnection.cursor()

        cursor.execute(SQL_GET_DATABASE)

        dados = cursor.fetchone()

        return traduzCheckDatabaseHealth(dados)

    def checkTablesHealth(self):
        mysqlConnection = GetMysqlConnection()
        cursor = mysqlConnection.cursor()

        cursor.execute(SQL_GET_TABLE)

        dados = cursor.fetchone()

        return traduzCheckTablesHealth(dados)


def traduzCheckDatabaseHealth(tupla):
    return 200 if tupla else 404


def traduzCheckTablesHealth(tupla):
    return 200 if tupla else 404
