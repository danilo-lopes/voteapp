from front import app
from dao import GetvotesFromSql
from flask_restful import Resource, Api

api = Api(app)


class Main(Resource):
    def get(self):
        return {'about': 'Vote App Viewer. To get quantity of votes, please query /api/votes'}


class GetVotes(Resource):
    def get(self):
        daoVotes = GetvotesFromSql()

        cocaVotes = str(daoVotes.getCocaVotes())
        pepsiVotes = str(daoVotes.getPepsiVotes())

        return {
            'votes':
                {
                    'coca': cocaVotes,
                    'pepsi': pepsiVotes
                },
        }, 200


api.add_resource(Main, '/api')
api.add_resource(GetVotes, '/api/votes')
