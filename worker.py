from calendar import c
import sys
import os
import django
import traceback
import json
import importlib
import time
from decouple import config

__ENV__ = os.environ.get("ENVIRONMENT","development")
if __ENV__ == 'development':    
    sys.path.insert(0, config('APP_ROOT'))
    sys.path.insert(1, config('APP_ROOT_APP'))
elif __ENV__ == 'production':
    sys.path.insert(0, '/code')

os.environ["DJANGO_SETTINGS_MODULE"] = "ttsapp.settings"

django.setup()
from django.conf import settings
from tasker import init_broker, logger

connection, channel = init_broker()

def main():
    queue = settings.TASKER['default_broker']['queue']
    def callback(ch, method, properties, body):
        task_json = json.loads(body)
        task_module = '{}'.format(task_json['module'])
        _module = importlib.import_module(task_module)
        args = json.loads(task_json['args'])
        kwargs = json.loads(task_json['kwargs'])
        _function = getattr(_module, task_json['name'])
        _function(*args, **kwargs)
        msg = "Running task... {}".format(kwargs)
        logger(msg, 'success', 'consumer')

    channel.queue_declare(queue=queue)
    channel.basic_consume(queue=queue, auto_ack=True, on_message_callback=callback)
    channel.start_consuming()
    time.sleep(20)

if __name__ == '__main__':
    try:
        main()
    except:
        msg = traceback.print_exc()
        logger(msg,'error','consumer')
