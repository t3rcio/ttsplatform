
import os
import requests
from bs4 import BeautifulSoup
from gtts import gTTS

from django.utils import timezone
from django.conf import settings

from app.core.models import RequestTTS, LANG
from app.monitor.models import TaskMonitor, FINISHED, STARTED, RUNNING, IDLE, FAILED


__all__ = ['obtem_texto', 'task_convert_url']

def obtem_texto(url:str) -> str:
	paragrafos = []
	if url != '':
		req = requests.get(url)
		if req.status_code == 200:
			html = req.text.encode('utf-8')
			parser = BeautifulSoup(html, 'html.parser')
			for p in parser.find_all('p'):
				paragrafos.append(p.get_text())
			return ''.join(paragrafos)
	return ''


def salva_tts(request_tts:RequestTTS) -> None:
	texto = request_tts.text
	_tss = gTTS(text=texto, lang=LANG, slow=False)
	file_path = '{}/{}.mp3'.format(settings.MEDIA_ROOT, request_tts.ide)
	_tss.save(file_path)
	return os.path.isfile(file_path)


def task_convert_url(*args, **kwargs):
	request_obj = kwargs.get('request_tts', None)
	print('tarefa recebida>> ' + str(request_obj))
	if request_obj:
		target = 'RequestTTS:{}'.format(request_obj['ide'])
		request_tts = RequestTTS.objects.get(ide=request_obj['ide'])
		novo_monitor = TaskMonitor.objects.create(target=target, progress=33, status=STARTED, descricao='Obtendo dados do texto...')
		texto = obtem_texto(url=request_obj['url'])
		novo_monitor.progress += 33
		novo_monitor.status = RUNNING
		novo_monitor.descricao = 'Convertendo para voz...'
		novo_monitor.save()
		request_tts.text = texto
		request_tts.save()
		res = salva_tts(request_tts=request_tts)
		if res:
			novo_monitor.status = FINISHED
			progresso_atual = novo_monitor.progress
			novo_monitor.progress += (100 - progresso_atual)
			novo_monitor.descricao = 'Concluindo...'
		else:
			novo_monitor.status = FAILED
		novo_monitor.save()





