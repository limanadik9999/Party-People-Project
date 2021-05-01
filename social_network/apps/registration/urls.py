from django.urls import path
from django.contrib.auth import views as standard_views
from . import views

app_name = 'registration'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', standard_views.LoginView.as_view(), name='login'),
    path('logout/', standard_views.LogoutView.as_view(), name='logout'),
    path('registration/', views.register, name = 'register'),
    ]
