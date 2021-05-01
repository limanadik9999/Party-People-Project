from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Event, Like, Comment
from account.models import Friend, Follower
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EventForm
from .forms import Event
from django.utils import timezone
from django.template.loader import render_to_string


@login_required(login_url = '/')
def delete_event(request, event_id):
    try:
        event = event.objects.get(id = event_id)
    except:
        raise Http404("Пост не найден!")
    if event.author == request.user:
        event.delete()
    return HttpResponseRedirect(reverse('account:user_account'))


@login_required(login_url = '/')
def edit_event(request, event_id):
    try:
        event = event.objects.get(id = event_id)
    except:
        raise Http404("Пост не найден!")

    if event.author == request.user:
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                event.event_title = form.cleaned_data['event_title']
                event.event_text = form.cleaned_data['event_text']
                image = form.cleaned_data['event_image']
                if image:
                    event.event_image = image
                else:
                    event.event_image = ''
                event.save()

                return HttpResponseRedirect(reverse('account:user_account'))
        else:
            form = EventForm(instance=event)
        context = {'form': form, "event": event}
        return render(request, 'events/edit_event.html', context)
    else:
        return HttpResponseRedirect(reverse('account:user_account'))


@login_required(login_url = '/')
def event(request, event_id):
    try:
        event = Event.objects.get(id = event_id)
    except:
        raise Http404("Пост не найден!")

    if request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/news'+str(event_id)+'/' or request.META.get('HTTP_REFERER') == 'http://mypineapple.pythonanywhere.com/news'+str(event_id)+'/':
        pass
    else:
        request.session['return_path'] = request.META.get('HTTP_REFERER','/')

    context = {"event": event}
    return render(request, 'events/event.html', context)


@login_required(login_url = '/')
def news(request):
    events = event.objects.all().exclude(author = request.user).order_by("-event_time")
    page = request.GET.get('page', 1)
    paginator = Paginator(events, 20)
    try:
      event_list = paginator.page(page)
    except PageNotAnInteger:
      event_list = paginator.page(1)
    except EmptyPage:
      event_list = paginator.page(paginator.num_pages)

    context = {'events': event_list}
    return render(request, 'events/news.html', context)


@login_required(login_url = '/')
def friend_news(request):
    events = Event.objects.all().exclude(author = request.user).order_by("-event_time")
    friend_event = []
    for event in events:
        if Friend.objects.filter(user = request.user, users_friend = event.author, confirmed = True)|Friend.objects.filter(user = event.author, users_friend = request.user, confirmed = True) or Follower.objects.filter(user = request.user, follower_for = event.author):
            friend_event.append(event)
    page = request.GET.get('page', 1)
    paginator = Paginator(friend_event, 20)
    try:
      event_list = paginator.page(page)
    except PageNotAnInteger:
      event_list = paginator.page(1)
    except EmptyPage:
      event_list = paginator.page(paginator.num_pages)

    follow_list = Follower.objects.filter(user = request.user)
    context = {'events': event_list, 'follow_list': follow_list}
    return render(request, 'events/friend_news.html', context)


@login_required(login_url = '/')
def like_news(request):
    like_events = request.user.event_liked.all().order_by("-event_time")
    page = request.GET.get('page', 1)
    paginator = Paginator(like_events, 20)
    try:
      event_list = paginator.page(page)
    except PageNotAnInteger:
      event_list = paginator.page(1)
    except EmptyPage:
      event_list = paginator.page(paginator.num_pages)

    context = {'events': event_list}
    return render(request, 'events/like_news.html', context)


@login_required(login_url = '/')
def like_or_dislike(request):
    event_id = request.POST.get('id')
    action = request.POST.get('action')
    if event_id and action:
        try:
            event = Event.objects.get(id=event_id)
            if action == 'like':
                event.event_like.add(request.user)
            else:
                event.event_like.remove(request.user)
            if action == 'dislike':
                event.event_dislike.add(request.user)
            else:
                event.event_dislike.remove(request.user)
                return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ok'})


@login_required(login_url = '/')
def user_like(request):
    likes = Like.objects.all()
    for like in likes:
        if like.like_or_dislike == "like":
            like.for_event.event_like.add(like.user)
        if like.like_or_dislike == "dislike":
            like.for_event.event_dislike.add(like.user)
    return HttpResponse("Complete")


@login_required(login_url = '/')
def leave_comment(request, event_id):
    try:
        event = Event.objects.get(id = event_id)
    except:
        raise Http404("Пост не найден!")

    if request.method == 'POST':
        comment_text = request.POST['comment_text']
        comment = event.event_comments.create(comment_author = request.user, comment_text = comment_text, comment_pubdate = timezone.now())

    if comment:
        context = {'comment': comment, 'event': event}
        return HttpResponse(
            json.dumps({
                "result": True,
                "comment": render_to_string('events/create_comment.html', context),
            }),
            content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({
                "result": False,
            }),
            content_type="application/json")


@login_required(login_url = '/')
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id = comment_id)
    except:
        raise Http404("Комментарий не найден!")
    if comment.comment_author == request.user:
        comment.delete()
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'no'})


def back(request):
    return redirect(request.session['return_path'])
