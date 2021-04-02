from rest_framework import serializers
from .models import Messages, Feedback, Topics

class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
      model = Topics
      fields = ['id','topic_name']


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ['id', 'is_liked', 'is_disliked', 'comment', 'username', 'message']


class MessagesSerializer(serializers.ModelSerializer):

    def _check_live_status(self):
        if (self.expiration_timestamp > timezone.now):
            return True
        else:
            return False


    feedbacks = FeedbackSerializer(source='feedback_set', many=True)

    class Meta:
        model = Messages
        fields = '__all__'
        #fields = ['post_identifier', 'topic', 'title', 'message', 'creation_timestamp', 'expiration_timestamp', 'username', 'feedbacks', 'likes', 'dislikes', 'total_interactions']
        depth = 1

   
