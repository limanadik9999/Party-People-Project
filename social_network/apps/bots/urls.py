from django.urls import path

from . import views

app_name = 'bots'
urlpatterns = [
    path('create_event/', views.create_event, name = 'create_event'),
    ]
