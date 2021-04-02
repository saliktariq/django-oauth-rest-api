from rest_framework import serializers
from .models import Messages, Feedback, Topics
import datetime
from django.utils import timezone




class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ['id', 'is_liked', 'is_disliked', 'comment', 'username', 'message']


class MessagesSerializer(serializers.ModelSerializer):
    live_status = serializers.SerializerMethodField('_check_live_status')

    def _check_live_status(self, messages_object):
        expiration_time = getattr(messages_object, "expiration_timestamp")
        if (expiration_time > timezone.now()):
            return True
        else:
            return False


    feedbacks = FeedbackSerializer(source='feedback_set', many=True)

    class Meta:
        model = Messages
        fields = ['post_identifier', 'topic', 'title', 'message', 'creation_timestamp', 'expiration_timestamp', 'username', 'likes', 'dislikes', 'total_interactions','feedbacks', 'live_status']
        depth = 1

   
class TopicsSerializer(serializers.ModelSerializer):
    messages = MessagesSerializer(source='messages_set', many=True)
    class Meta:
      model = Topics
      fields = ['id','topic_name','messages']
