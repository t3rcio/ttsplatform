import json

from django.db import models
from django.utils import timezone
from datetime import datetime

FINISHED = 'FINISHED'
STARTED = 'STARTED'
RUNNING = 'RUNNING'
IDLE = 'IDLE'
FAILED = 'FAILED'

class TaskMonitor(models.Model):
	# - target salva o objeto a monitorar
	# - Classe:valor_pk
	target = models.CharField(max_length=256, default='')
	data = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=32, default=IDLE)
	progress = models.IntegerField(default=0)

	def parse_target(self) -> tuple:
		return self.target.split(':')

	def to_json(self):
		return json.dumps({
			'ide': self.ide,
			'data': self.data,
			'status': self.status,
			'progress': self.progress
			})

	class Meta:
		ordering = ['-data']


