from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.core import validators
from django.core.exceptions import ValidationError
#from django.utils.translation import gettext_lazy as _


class Messages(models.Model):

    post_identifier = models.AutoField(primary_key=True)
    topic = models.ManyToManyField('Topics')
    title = models.CharField(max_length=100)
    message = models.TextField()
    creation_timestamp = models.DateTimeField(default=timezone.now)
    expiry_in_seconds = models.DateTimeField()
    username = models.CharField(max_length=100)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    total_interactions = models.PositiveIntegerField(default=0)



    def __str__(self):
        return self.title


class Topics(models.Model):
    TOPICS = [('P', 'Politics'), ('H', 'Health'), ('S', 'Sports'), ('T', 'Tech')]
    topic_name = models.CharField(max_length=2, unique=True, choices=TOPICS)

    def __str__(self):
        return self.topic_name


class Feedback(models.Model):

    is_liked = models.BooleanField(default=False, blank=True)
    is_disliked = models.BooleanField(default=False, blank=True)
    comment = models.TextField(blank=True)
    username = models.CharField(max_length=100)
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
