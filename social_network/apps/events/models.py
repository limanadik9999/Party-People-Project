from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    event_title = models.CharField('Title', max_length = 150, blank = True)
    event_text = models.TextField('Description')
    event_image = models.ImageField('Image', blank = True, upload_to = 'images/event/')
    event_image_url = models.ImageField('URL image', blank = True)
    event_time = models.DateTimeField('Creation date')
    event_like = models.ManyToManyField(User,
                                        related_name='event_liked',
                                        blank=True)
    event_dislike = models.ManyToManyField(User,
                                        related_name='event_disliked',
                                        blank=True)

    def __str__(self):
        return str(self.author)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class Like(models.Model):
    LIKE_OR_DISLAKE_CHOICES = (
    ("LIKE", "like"),
    ("DISLIKE", "dislike"),
    (None, "None")
    )

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    for_event = models.ForeignKey(Event, on_delete = models.CASCADE)
    like_or_dislike = models.CharField(max_length=7,
                  choices=LIKE_OR_DISLAKE_CHOICES,
                  default=None)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE, related_name="event_comments")
    comment_author = models.ForeignKey(User, on_delete = models.CASCADE)
    comment_text = models.CharField('Text of comment', max_length = 350)
    comment_pubdate = models.DateTimeField('Publication date')

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comment'
