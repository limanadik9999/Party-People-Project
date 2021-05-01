from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone
from datetime import datetime, timedelta


class Profile(models.Model):
    GENDER_CHOICE = (
    ("M", "Male"),
    ("F", "Female"),
    (None, "-")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField('Avatar', blank=True, upload_to = 'images/avatar/')
    gender =  models.CharField('Sex', max_length=1,
                  choices=GENDER_CHOICE,
                  blank=True)
    city = models.CharField('City', max_length=100, blank=True)
    birth_date = models.DateField('Birthday', null=True, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Status(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    online = models.DateTimeField('Was online', null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_online_status(self):
        status = ''
        timezone_delta = timedelta(hours=3, minutes=0)
        online_status_true = timedelta(minutes=5)
        user_online = self.online + timezone_delta

        # if self.user.profile.gender == 'F':
        #     if user_online.date() == (datetime.now() - timedelta(days=1)).date():
        #         status = 'Была онлайн вчера в ' + user_online.time().strftime("%H:%M")
        #     elif timezone.now() - self.online < online_status_true:
        #         status = 'Онлайн'
        #     elif user_online.date() == datetime.now().date():
        #         status = 'Была онлайн сегодня в ' + user_online.time().strftime("%H:%M")
        #     elif user_online.date().year == datetime.now().date().year:
        #         status = 'Была онлайн ' + user_online.date().strftime("%d.%m") + ' в ' + user_online.time().strftime("%H:%M")
        #     else:
        #         status = 'Была онлайн ' + user_online.date().strftime("%d.%m.%Y") + ' в ' + user_online.time().strftime("%H:%M")
        # else:
        if user_online.date() == (datetime.now() - timedelta(days=1)).date():
                status = 'Was online yesterday at ' + user_online.time().strftime("%H:%M")
        elif timezone.now() - self.online < online_status_true:
                status = 'Online'
        elif user_online.date() == datetime.now().date():
                status = 'Was online today at ' + user_online.time().strftime("%H:%M")
        elif user_online.date().year == datetime.now().date().year:
                status = 'Was online ' + user_online.date().strftime("%d.%m") + ' в ' + user_online.time().strftime("%H:%M")
        else:
                status = 'Was online ' + user_online.date().strftime("%d.%m.%Y") + ' в ' + user_online.time().strftime("%H:%M")
        return status

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    users_friend = models.ForeignKey(User, related_name = 'users_friend', on_delete = models.CASCADE)
    confirmed = models.BooleanField('Confirmed', default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    follower_for = models.ForeignKey(User, related_name = 'follower_for', on_delete = models.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'
