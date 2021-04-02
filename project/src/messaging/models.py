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



    # def post_live_time_remaining(self):
    #     if (self.expiration_timestamp > timezone.now):
    #         return (self.expiration_timestamp - timezone.now).total_seconds()
    #     else:
    #         return 0

    # def get_username(request):
    #     current_user = request.user
    #     return current_user.username

    # def get_user_id(request):
    #     current_user = request.user
    #     return current_user.id

    post_identifier = models.AutoField(primary_key=True)
    topic = models.ManyToManyField('Topics')
    title = models.CharField(max_length=100)
    message = models.TextField()
    creation_timestamp = models.DateTimeField(default=timezone.now)
    expiration_timestamp = models.DateTimeField()
    username = models.CharField(max_length=100)
    #######testing new fields#######
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    total_interactions = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        # if not self.is_live:
        #     self.is_live = self.post_live_status()

        if not self.expiration_timestamp:
            self.expiration_timestamp = self.expiration_time_calculation()

        # if not self.username:
        #     self.username = self.get_username()

        # if not self.user_id:
        #     self.user_id = self.get_user_id()

        super(Messages, self).save(*args, **kwargs)

    # def post_live_status(self):
    #     if (self.expiration_timestamp > timezone.now):
    #         return True
    #     else:
    #         return False

    # def save(self, *args, **kwargs):
    #     if not self.is_live:
    #         self.is_live = self.post_live_status()
    #     super(Messages, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Topics(models.Model):
    TOPICS = [('P', 'Politics'), ('H', 'Health'), ('S', 'Sports'), ('T', 'Tech')]
    topic_name = models.CharField(max_length=2, unique=True, choices=TOPICS)

    def __str__(self):
        return self.topic_name


class Feedback(models.Model):

    # def get_username(request):
    #     current_user = request.user
    #     return current_user.username

    # def get_user_id(request):
    #     current_user = request.user
        # return current_user.id

    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    username = models.CharField(max_length=100)
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     if not self.username:
    #         self.username = self.get_username()

    #     if not self.user_id:
    #         self.user_id = self.get_user_id()

    #     super(Feedback, self).save(*args, **kwargs)

    def __str__(self):
        return self.comment
