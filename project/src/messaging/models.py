from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Messages(models.Model):

    def expiration_time_calculation(self):
        EXPIRATION_DURATION = 86400  # time in seconds
        expiration_time = self.creation_timestamp + timedelta(seconds=EXPIRATION_DURATION)
        return expiration_time



    post_identifier = models.AutoField(primary_key=True)
    topic = models.ManyToManyField('Topics')
    title = models.CharField(max_length=100)
    message = models.TextField()
    creation_timestamp = models.DateTimeField(default=timezone.now())
    expiration_timestamp = models.DateTimeField()
    username = models.CharField(max_length=100)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    total_interactions = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):

        if not self.expiration_timestamp:
            self.expiration_timestamp = self.expiration_time_calculation()
        super(Messages, self).save(*args, **kwargs)


    def __str__(self):
        return self.title


class Topics(models.Model):
    TOPICS = [('P', 'Politics'), ('H', 'Health'), ('S', 'Sports'), ('T', 'Tech')]
    topic_name = models.CharField(max_length=2, unique=True, choices=TOPICS)

    def __str__(self):
        return self.topic_name


class Feedback(models.Model):

    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    username = models.CharField(max_length=100)
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
