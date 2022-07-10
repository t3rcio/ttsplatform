
import json
import pika
from tasker import logger, init_broker
from django.conf import settings

def publisher(function, *args, **kwargs):
    exchange = settings.TASKER['default_broker']['exchange']
    task = {
        'name': '',
        'module': '',
        'args':[],
        'kwargs': {}
    }
    connection, channel = init_broker()
    def wrapper(*args, **kwargs):
        task['name'] = function.__name__
        task['module'] = function.__module__
        task['args'] = json.dumps(args)
        task['kwargs'] = json.dumps(kwargs)
        task_json = json.dumps(task)
        channel.basic_publish(exchange=exchange,routing_key='tasks', body=task_json,properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        msg = 'Task: {} sent'.format(task['name'])
        logger(msg, 'success')
        connection.close()
    return wrapper(*args, **kwargs)





