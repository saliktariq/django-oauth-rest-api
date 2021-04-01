from rest_framework import serializers
from .models import Messages, Feedback, Topics

class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
      model = Topics
      fields = ['id','topic_name']


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ['id', 'is_liked', 'is_disliked', 'comment', 'username', 'user_id']


class MessagesSerializer(serializers.ModelSerializer):
    feedbacks = FeedbackSerializer(source='feedback_set', many=True)
    class Meta:
        model = Messages
        fields = ['post_identifier', 'topic', 'title', 'message', 'creation_timestamp', 'expiration_timestamp', 'is_live', 'username', 'user_id', 'feedbacks']