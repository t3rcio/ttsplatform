
import os
from django.test import TestCase
from django.conf import settings

from app.core.models import RequestTTS
from app.tasks import obtem_texto, task_convert_url

class TestRequestTTS(TestCase):

	def setUp(self, *args, **kwargs):
		pass

	def test_save_RequestTTS(self):
		request = RequestTTS(url='https://some.url.com')
		request.save()
		assert request.ide != ''
		assert request.data is not None
		

class TestTasks(TestCase):

	def setUp(self):
		self.request_tts = RequestTTS.objects.create(
			url='https://jw.org/pt',
			)

	def test_obtem_texto(self):
		texto = obtem_texto(url=self.request_tts.url)
		assert texto != ''
		assert len(texto) > 1

	def test_task_convert_url(self):
		file_path = '{}/{}.mp3'.format(settings.MEDIA_ROOT, self.request_tts.ide)
		task_convert_url(request_tts=self.request_tts)
		assert os.path.isfile(file_path)

