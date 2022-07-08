
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from app.core.models import RequestTTS
from app.tasks import task_convert_url
from tasker.publisher import publisher

@receiver(post_save, sender=RequestTTS)
def cria_tarefa(sender, instance, created, **kwargs):
    if created:
        request_dict = instance.to_dict()
        # - publisher(task_convert_url, **{'request_tts':request_dict})
        # - task_convert_url(**{'request_tts':instance})
