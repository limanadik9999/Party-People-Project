from django.shortcuts import render
import requests

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from events.models import Event
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def create_event(request):
    user = User.objects.get(username = 'bot')
    #token не работает, так как подкорректирован. У вас должен быть свой
    token = 'f88de38bf88de38bf88de38bd3f8fc7a6fff88df88de38ba620dc9725559b497361de40'
    version = 5.103
    domain = 'tproger'

    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                            'access_token': token,
                            'v': version,
                            'domain': domain,
                            'count': 5
                            }
                        )
    data = response.json()['response']['items']
    for news in data:
        try:
            if news['attachments'][0]['type']:
                img_url = news['attachments'][0]['photo']['sizes'][-1]['url']
            else:
                img_url = ''
        except:
            img_url = ''

        try:
            news['attachments'][0]['video']
        except:
            if news['text'] != '':
                in_event = Event.objects.filter(event_text = news['text'])
            else:
                in_event = Event.objects.filter(event_image_url = img_url)

            if not in_event:
                event = Event(author = user, event_text=news['text'], event_time = timezone.now(), event_image_url=img_url)
                event.save()

    return HttpResponse('Complete ')
