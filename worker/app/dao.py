from dataBases import GetMysqlConnection

SQL_REGISTER_VOTE = 'INSERT into votes (userID, vote) values (%s, %s)'
SQL_UPDATE_VOTE = 'UPDATE votes SET vote=%s where userID = %s'
SQL_GET_VOTE = 'SELECT userID from votes where userID = %s'


class VotingDao:
    def registerVote(self, userID, vote):
        if userID == self.getVote(userID):
            self.updateVote(userID, vote)
        else:
            mysqlConnection = GetMysqlConnection()
            cursor = mysqlConnection.cursor()

            cursor.execute(SQL_REGISTER_VOTE, (userID, vote))
            mysqlConnection.commit()

    def getVote(self, userID):
        mysqlConnection = GetMysqlConnection()
        cursor = mysqlConnection.cursor()

        cursor.execute(SQL_GET_VOTE, (userID,))

        dados = cursor.fetchone()

        return traduzGetVote(dados)

    def updateVote(self, userID, vote):
        mysqlConnection = GetMysqlConnection()
        cursor = mysqlConnection.cursor()

        cursor.execute(SQL_UPDATE_VOTE, (vote, userID))

        mysqlConnection.commit()


def traduzGetVote(tupla):
    return tupla[0] if tupla else None
