from rest_framework import serializers
from .models import Messages, Feedback, Topics
import datetime
from django.utils import timezone
from datetime import timedelta


"""
FeedbackSerializer used to serialize Feedback class
"""

class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ['id', 'is_liked', 'is_disliked', 'comment', 'username', 'message']

"""
MessagesSerializer used to serialize Messages class
"""
class MessagesSerializer(serializers.ModelSerializer):
    #Following SerializerMethodField keeps value of status of a message, i.e., whether a post is live or expired
    #If it is False, the post is expired, if it is True, the post is Live
    live_status = serializers.SerializerMethodField('_check_live_status')
    #Following SerializerMethondField contains the remaining time in seconds before a message will expire
    live_time_remaining = serializers.SerializerMethodField('_check_remaining_time')

    #Serializer method that compares the expiry time with current time to determine live status of a post, i.e., whether a post is live or expired
    def _check_live_status(self, messages_object):
        expiration_time = getattr(messages_object, "expiry_in_seconds")
        if (expiration_time > timezone.now()):
            return True
        else:
            return False
    #Serializer method that calculates remaining time before a post will expire. This method will subtract expiry time from current time to calculate 
    #post's live remaining time. If a post is expired it will simply return 0 instead of negative time.
    def _check_remaining_time(self, messages_object):
        expiration_time = getattr(messages_object, "expiry_in_seconds")
        remaining_time = expiration_time - timezone.now()
        if(remaining_time.total_seconds() < 0):
            return 0
        else:
            return remaining_time
        

    feedbacks = FeedbackSerializer(source='feedback_set', many=True)

    class Meta:
        model = Messages
        fields = ['post_identifier', 'topic', 'title', 'message', 'creation_timestamp', 'expiry_in_seconds', 'username', 'likes', 'dislikes', 'total_interactions','feedbacks', 'live_status', 'live_time_remaining']
        depth = 1
        #Depth = 1 will help access whole Feedback objects in JSON associated with a message

"""
TopicsSerializer used to serialize Topics class
"""
   
class TopicsSerializer(serializers.ModelSerializer):
    #Creating  messages field representing associated Messages object
    messages = MessagesSerializer(source='messages_set', many=True)
    class Meta:
      model = Topics
      #Adding extra field messages here to be able to perform reverse lookup Topic -> Messages, although it is not required, added this as an extra feature.
      fields = ['id','topic_name','messages']
