
from django.conf import settings
from datetime import datetime

import sys
import pika
import traceback

def logger(msg:str, type:str, source='tasker') -> None:
    try:
        _file = '{}/{}_{}.log'.format(settings.APP_LOGPATH,datetime.now().strftime('%Y_%m_%d'), source)
        _type = '[{}]'.format(type.upper())
        with open(_file, 'a') as logfile:
            logfile.write('{} - {}  - {}\n'.format(datetime.now(), _type, msg))
    except:
        traceback.print_exc(file=sys.stderr)
        


def init_broker() -> tuple:
    exchange = settings.TASKER['default_broker']['exchange']
    credentials = pika.PlainCredentials(
        settings.TASKER['default_broker']['username'],
        settings.TASKER['default_broker']['password'],
    )

    parameters = pika.ConnectionParameters(
        settings.TASKER['default_broker']['host'],
        credentials=credentials
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    try:
        channel.queue_declare(queue=settings.TASKER['default_broker']['queue'])
        channel.exchange_declare(exchange=exchange, exchange_type='fanout', durable=True)
        channel.queue_bind(exchange=exchange, queue=settings.TASKER['default_broker']['queue'])
    except ValueError:
        traceback.print_exc(file=sys.stderr)
        msg = traceback.print_exc()
        logger(msg=msg, type='error')
    return connection, channel
