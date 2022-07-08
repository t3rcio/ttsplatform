
from django.urls import path
from app.core.views import index, tts, monitoring

urlpatterns = [
    path('', index, name='home'),
    path('monitoring/<str:ide>', monitoring, name='monitoring'),
    path('ide/<str:ide>', tts, name='tts'),
]