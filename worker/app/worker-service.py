from models import Message, QueueService, MessageRepository
from dataBases import sqsConnection
import datetime
import time

sqsConnection = sqsConnection()

queueService = QueueService(sqsConnection)
serviceRepository = MessageRepository()

while True:
    queueMessages = queueService.getMessageFromSqs()

    for message in queueMessages:
        sqsMessage = Message(body=message.body, messageID=message.message_id, receiptHandle=message.receipt_handle)

        if sqsMessage.body:

            if not serviceRepository.storeMessageIntoDatabase(sqsMessage):
                queueService.deleMessagesFromSqsQueue(sqsMessage)

            else:
                now = str(datetime.datetime.now()).split('.')[0]

                file = open('workerServiceLog/workerservicelog.log', 'a')

                message = f'\n {now} unbale to process vote into MYSQL. {serviceRepository.storeMessageIntoDatabase(sqsMessage)}'

                file.write(message)

                file.close()

                time.sleep(1)

    continue
