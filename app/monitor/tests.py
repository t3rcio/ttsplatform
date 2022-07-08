
import os
import subprocess
import requests
from django.test import TestCase

from app.core.models import RequestTTS
from app.monitor.models import TaskMonitor, RUNNING, FINISHED
from app.tasks import task_convert_url
from notifier_app.server import APP_PATH

class TestTaskMonitor(TestCase):

	def setUp(self):
		self.monitor = TaskMonitor.objects.create(
			target="RequestTTS:321-654-987-anbv4dada54"
			)
		self.request_tts = RequestTTS.objects.create(
			url="https://www.lipsum.com/"
			)

	def test_taskmonitor_target(self):
		_class, ide = self.monitor.parse_target()
		assert _class == 'RequestTTS'
		assert ide != ''

	def test_taskmonitor_progress(self):
		target = "RequestTTS:{}".format(self.request_tts.ide)
		task_convert_url(**{'request_tts':self.request_tts})
		task_monitor = TaskMonitor.objects.filter(target=target)
		assert task_monitor.count() > 0
		assert task_monitor.first() is not None
		while task_monitor.first().progress < 100:
			assert task_monitor.first().status == RUNNING
		assert task_monitor.first().status == FINISHED


class TestTaskMonitorServer(TestCase):

	def setUp(self):
		os.environ["ENVIRONMENT"] = "testing"
		script = os.path.join(APP_PATH, 'notifier_app/run.py')
		subprocess.run(["python", script])
		

	def test_notifer_server(self):
		url = 'http://localhost:8080/testme'
		req = requests.get(url)
		assert req.status_code == 200
		assert req.text == 'It Works!'


