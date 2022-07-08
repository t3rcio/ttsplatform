
from django.db import models
from django.utils import timezone
import uuid

LANG = 'pt-br'

class RequestTTS(models.Model):
	ide = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	url = models.URLField(max_length=256)
	text = models.TextField(blank=True, null=True, default='')
	mp3 = models.CharField(max_length=1024, default='')
	language = models.CharField(max_length=256, default='pt-br')
	data = models.DateTimeField(default=timezone.now)

	class Meta:
		verbose_name = 'Requisição'
		verbose_name_plural = 'Requisições'

	def to_dict(self):
		return {
			'ide': self.ide.__str__(),
			'url': self.url,
		}
