import socket
import random
import json
from voting import app, getSqsConnection
from flask import render_template, request, make_response

title = 'Voting App'
hostname = socket.gethostname()
optionA = 'Coca'
optionB = 'Pepsi'


@app.route('/', methods=['POST', 'GET'])
def index():
    userID = request.cookies.get('userID')

    if not userID:
        userID = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        sqs = getSqsConnection()

        vote = request.form['vote']

        data = json.dumps(
            {
                'userID': userID,
                'vote': vote
            }
        )

        queueUrl = sqs.get_queue_url(QueueName='voting')['QueueUrl']

        sqs.send_message(
            QueueUrl=queueUrl,
            DelaySeconds=1,
            MessageBody=data
        )

    response = make_response(
        render_template(
            'index.html',
            title=title,
            hostname=hostname,
            optionA=optionA,
            optionB=optionB,
            vote=vote
        )
    )

    response.set_cookie('userID', userID)

    return response
