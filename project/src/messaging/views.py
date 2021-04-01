from rest_framework import viewsets
from .serializers import MessagesSerializer, FeedbackSerializer, TopicsSerializer
from .models import Messages, Feedback, Topics
from django.contrib.auth.models import User

class MessagesViewset(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer

    def get_queryset(self):
        messages = Messages.objects.all()
        return messages
