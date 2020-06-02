from models import Message, QueueService, MessageRepository
from dataBases import sqsConnection

sqsConnection = sqsConnection()

queueService = QueueService(sqsConnection)
serviceRepository = MessageRepository()

while True:
    queueMessages = queueService.getMessageFromSqs()

    for message in queueMessages:
        sqsMessage = Message(body=message.body, messageID=message.message_id, receiptHandle=message.receipt_handle)

        if sqsMessage.body:
            serviceRepository.storeMessageIntoDatabase(sqsMessage)

            queueService.deleMessagesFromSqsQueue(sqsMessage)

    continue
