from dataBases import GetMysqlConnection

SQL_REGISTER_VOTE = 'INSERT into voteapp.votes (userID, vote) values (%s, %s)'
SQL_UPDATE_VOTE = 'UPDATE voteapp.votes SET vote=%s where userID = %s'
SQL_GET_VOTE = 'SELECT userID from voteapp.votes where userID = %s'


class VotingDao:
    def registerVote(self, userID, vote):
        try:
            if userID == self.getVote(userID):
                self.updateVote(userID, vote)
            else:
                mysqlConnection = GetMysqlConnection()
                cursor = mysqlConnection.cursor()

                cursor.execute(SQL_REGISTER_VOTE, (userID, vote))
                mysqlConnection.commit()

        except Exception as erro:
            return erro

    def getVote(self, userID):
        try:
            mysqlConnection = GetMysqlConnection()
            cursor = mysqlConnection.cursor()

            cursor.execute(SQL_GET_VOTE, (userID,))

            dados = cursor.fetchone()

            return traduzGetVote(dados)

        except Exception as erro:
            return erro

    def updateVote(self, userID, vote):
        try:
            mysqlConnection = GetMysqlConnection()
            cursor = mysqlConnection.cursor()

            cursor.execute(SQL_UPDATE_VOTE, (vote, userID))

            mysqlConnection.commit()

        except Exception as erro:
            return erro


def traduzGetVote(tupla):
    return tupla[0] if tupla else None
