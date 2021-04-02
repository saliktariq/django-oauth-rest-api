from rest_framework import serializers
from .models import Messages, Feedback, Topics
import datetime
from django.utils import timezone
from datetime import timedelta




class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ['id', 'is_liked', 'is_disliked', 'comment', 'username', 'message']


class MessagesSerializer(serializers.ModelSerializer):
    live_status = serializers.SerializerMethodField('_check_live_status')
    live_time_remaining = serializers.SerializerMethodField('_check_remaining_time')

    def _check_live_status(self, messages_object):
        expiration_time = getattr(messages_object, "expiry_in_seconds")
        if (expiration_time > timezone.now()):
            return True
        else:
            return False

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

   
class TopicsSerializer(serializers.ModelSerializer):
    messages = MessagesSerializer(source='messages_set', many=True)
    class Meta:
      model = Topics
      fields = ['id','topic_name','messages']
