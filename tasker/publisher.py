
import json
import pika
from tasker import logger, init_broker

def publisher(function, *args, **kwargs):
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
        print(task_json)
        channel.basic_publish(exchange='samp',routing_key='tasks', body=task_json,properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        msg = 'Task: {} sent'.format(task['name'])
        logger(msg, 'success')
        connection.close()
    return wrapper(*args, **kwargs)





