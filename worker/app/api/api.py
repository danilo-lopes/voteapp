from flask_restful import Resource, Api
from worker import app
from api.apiSqsService import ApiSqsService
from api.apiMysqlService import ApiMysqlService

api = Api(app)
sqsService = ApiSqsService()
mysqlService = ApiMysqlService()


class HealthCheckSqs(Resource):
    def get(self):
        queueStatus = sqsService.checkVotingSqsQueueHealth()

        if queueStatus == 200:
            return {
                'sqsStatus': 'OK'
            }, 200

        else:
            return {
                'sqsStatus': 'NOK'
            }


class HealthCheckMysql(Resource):
    def get(self):
        dataBaseStatus = mysqlService.checkDatabaseHealth()
        dataBaseTablesStatus = mysqlService.checkTablesHealth()

        if dataBaseStatus == 200 and dataBaseTablesStatus == 200:
            return {
                'mysqlStatus': 'OK'
            }

        else:
            return {
                'mysqlStatus': {
                    'database': dataBaseStatus,
                    'tables': dataBaseTablesStatus
                }
            }


api.add_resource(HealthCheckSqs, '/api/healthchecksqs')
api.add_resource(HealthCheckMysql, '/api/healthcheckmysql')
