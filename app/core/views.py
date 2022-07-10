
from django.http.response import JsonResponse
from django.shortcuts import render
from django.conf import settings

from app.core.models import RequestTTS
from app.monitor.models import RUNNING, TaskMonitor, STARTED, FINISHED
from app.tasks import task_convert_url
from tasker.publisher import publisher

def index(request, **kwargs):
    contexto = {
        'APP_URL':settings.APP_URL,
    }
    if request.method == 'POST':		
        url_input = request.POST.get('url','')
        if url_input != '':
            new_request = RequestTTS(url=url_input)
            new_request.save()
            contexto = {
                'APP_URL':settings.APP_URL,
                'ide': new_request.ide
            }
            publisher(task_convert_url, **{'request_tts':new_request.to_dict()})
    return render(request, 'index.html', contexto)


def monitoring(request, **kwargs):
    ide = kwargs.get('ide', '')
    res = {}
    if ide != '':
        query = request.GET.get('query','')
        if query == 'progress':
            monitor = TaskMonitor.objects.filter(target='RequestTTS:{}'.format(ide))
            if monitor.count() > 0:
                monitor = monitor.first()
                res = {'progress': monitor.progress, 'descricao':monitor.descricao}
                if monitor.progress == 100:
                    res = {'loadaudio':ide, 'progress':100, 'descricao':monitor.descricao}
    return JsonResponse(res)	


def tts(request, **kwargs):
    ide = kwargs.get('ide','')
    contexto = {}
    if ide != '':
        requesttts = RequestTTS.objects.get(ide=ide)
        contexto = {
            'tts': requesttts,
        }
    return render(request, 'result.html', contexto)
