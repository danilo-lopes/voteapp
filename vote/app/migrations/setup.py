import datetime
from prepare_sqs import createQueue

print('Dealing with SQS queue creation. To see what happen see migrationLog/migration.log')

try:

    result = createQueue()
    open("migrationLog/migration.log","w+")

    if result == 200:
        now = str(datetime.datetime.now()).split('.')[0]

        file = open('migrationLog/migration.log', 'a')

        message = f'\n {now} queue voting created successfully'

        file.write(message)

        file.close()

    elif result == 'voting':
        now = str(datetime.datetime.now()).split('.')[0]

        file = open('migrationLog/migration.log', 'a')

        message = f'\n {now} queue voting already exists'

        file.write(message)

        file.close()


except Exception as erro:
    now = str(datetime.datetime.now()).split('.')[0]

    file = open('migrationLog/migration.log', 'a')

    message = f'\n {now} {erro}'

    file.write(message)

    file.close()
