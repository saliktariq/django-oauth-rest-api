from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta #required to add extra time to current datetime object
from django.utils import timezone
from django.core import validators
from django.core.exceptions import ValidationError 

"""
Messages class is responsible of storing all the messages/posts in Piazza system.
"""

class Messages(models.Model):
    #This field acts as primary key and identifies a message.
    post_identifier = models.AutoField(primary_key=True)
    #This many to many relation field allows user to choose more than one topics for a message
    topic = models.ManyToManyField('Topics')
    #This field is used to store 'title' of a Message
    title = models.CharField(max_length=100)
    #This field is used to store message.
    message = models.TextField()
    #Creation timestamp is set to current date/time by default. No need to send this object in JSON when creating new object
    creation_timestamp = models.DateTimeField(default=timezone.now)
    #This field adds expiration time to the message. This calculation is done in messaging.views module
    expiry_in_seconds = models.DateTimeField()
    #The field saves current interacting user. This value is picked from Request object in messaging.views
    username = models.CharField(max_length=100)
    #This field keeps track of number of likes received on a post. Saves expensive iterative call / processing by keeping this number handy.
    likes = models.PositiveIntegerField(default=0)
    #This field keeps track of number of dislikes received on a post. Saves expensive iterative call / processing by keeping this number handy.
    dislikes = models.PositiveIntegerField(default=0)
    #This field contains TOTAL NUMBER OF INTERACTIONS on a post. That is the number of events a like/dislike/comment was made on a post.
    total_interactions = models.PositiveIntegerField(default=0)



    def __str__(self):
        return self.title

"""
Topics class contains a list of predefined topics that a user can choose for her messages / posts 
This class is connected with Messages class on Many-to-Many basis. I have also included reverse lookup endpoint in the API as well,
that could utilise this many to many relationship and retrieve all messages belonging to a particular topic.
"""
class Topics(models.Model):
    #Predefined list of topics. Topics may only be selected from following four options.
    TOPICS = [('P', 'Politics'), ('H', 'Health'), ('S', 'Sports'), ('T', 'Tech')]
    #This unique field contains the topic name. Kept it unique to facilitate reverse lookup functionality in the API 
    topic_name = models.CharField(max_length=2, unique=True, choices=TOPICS)

    def __str__(self):
        return self.topic_name

"""
Feedback class holds all user interactions to a particular posts and is associated to the message on Many:1 relationship basis.
"""

class Feedback(models.Model):
    #If user likes a post, turn this field to true
    is_liked = models.BooleanField(default=False, blank=True)
    #If user dislikes a post, turn this field to true
    is_disliked = models.BooleanField(default=False, blank=True)
    #This field contains comments made on user post
    comment = models.TextField(blank=True)
    #This field contains the username of the user who leaves feedback/comment.
    username = models.CharField(max_length=100)
    #Many to one field associating Feedback class to Messages class
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
