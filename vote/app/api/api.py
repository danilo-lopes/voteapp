from flask_restful import Resource, Api, request
from api.apiService import QueueService
from voting import app
import json

api = Api(app)
apiService = QueueService()


class PostVotes(Resource):
    def post(self):
        if request.method == 'POST':
            vote = request.get_json()

            userVote = json.dumps(vote)

            if apiService.checkIfMessageIsValid(userVote) == 200:

                userVote = apiService.sendMessage(userVote)

                try:
                    if userVote == 200:
                        return {
                            'voteStatus': 200
                        }

                except Exception as erro:
                    return erro

            return {
                'badRequest': 'Your json doesnt pass in the application creteria'
            }, 400

        else:
            return {
                'badRequest': 'unknown operation'
            }, 400


class HealthCheck(Resource):
    def get(self):

        queueStatus = apiService.checkVotingSqsQueueHealth()

        if queueStatus == 200:
            return {
                'sqsStatus': 'OK'
            }

        else:
            return {
                'sqsStatus': 'NOK'
            }


api.add_resource(PostVotes, '/api/postVotes')
api.add_resource(HealthCheck, '/api/healthcheck')
