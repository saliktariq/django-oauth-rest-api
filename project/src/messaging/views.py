from rest_framework import viewsets
from .serializers import MessagesSerializer, FeedbackSerializer, TopicsSerializer
from .models import Messages, Feedback, Topics
from django.contrib.auth.models import User
from rest_framework.response import Response
from datetime import timedelta
import datetime
import pytz
from django.utils import timezone

class MessagesViewset(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer

    def get_queryset(self):
        messages = Messages.objects.all()
        return messages

    #Learnt by following https://www.youtube.com/watch?v=ws0jwg1J0BU&list=PLmDLs7JbXWNjr5vyJhfGu69sowgIUl8z5&index=12
    def retrieve(self, request, *args, **kwargs): 
        parameters = kwargs
        message = Messages.objects.filter(post_identifier = parameters['pk'])
        serializer = MessagesSerializer(message) # use extra argument many=True if expecting multiple records
        return Response(serializer.data)

    #Learnt by following https://www.youtube.com/watch?v=4dPVywV-X84&list=PLmDLs7JbXWNjr5vyJhfGu69sowgIUl8z5&index=14
    def create(self, request, *args, **kwargs):
        message_data = request.data
        if('expiration_timestamp' in message_data):
            new_message = Messages.objects.create(title=message_data['title'], message= message_data['message'],  expiration_timestamp= message_data['expiration_timestamp'], username= request.user.username)
        else:
            new_message = Messages.objects.create(title=message_data['title'], message= message_data['message'], username= request.user.username)
        new_message.save()

        for topic in message_data['topic']:

            topic_object = Topics.objects.get(topic_name = topic['topic_name'])
            new_message.topic.add(topic_object)

        serializer = MessagesSerializer(new_message)
        return Response(serializer.data)

class TopicsViewset(viewsets.ModelViewSet):
    serializer_class = TopicsSerializer

    def get_queryset(self):
        topics = Topics.objects.all()
        return topics

    
    def retrieve(self, request, *args, **kwargs): 
        parameters = kwargs
        topic = Messages.objects.filter(topic_name = parameters['pk'])
        serializer = TopicsSerializer(topic, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        topic_data = request.data
        new_topic = Topics.objects.create(topic_name=topic_data['topic_name'])
        new_topic.save()

        serializer = TopicsSerializer(new_topic)
        return Response(serializer.data)

class FeedbackViewset(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        feedback = Feedback.objects.all()
        return feedback

    
    def retrieve(self, request, *args, **kwargs): 
        parameters = kwargs
        message_object = Messages.objects.filter(post_identifier = parameters['pk'])
        feedback_data = message_object['feedbacks']
        serializer = MessagesSerializer(feedback_data, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        feedback_data = request.data
        message_object = Messages.objects.filter(post_identifier=feedback_data['post_identifier']).first()

#check who is posting the message
        if (request.user.username == message_object.username):
            return Response(
                {
                    "Error: ": "Can not give feedback on own post"
                }
            )

        utc = pytz.UTC

        if(timezone.now() > message_object.expiration_timestamp):
            return Response(
                {
                    "Error: ": "Post is expired now, can not add comments."
                }
            )
 #check if user is not liking and disliking at the same time
        if (feedback_data['is_liked'] and feedback_data['is_disliked']):
            return Response(
                {
                    "Error: ": "Post can not be liked and disliked at the same time."
                }
            )
        

        
       
        new_feedback = Feedback.objects.create(is_liked= feedback_data['is_liked'],is_disliked= feedback_data['is_disliked'], comment= feedback_data['comment'], username= request.user.username, message=message_object)
        new_feedback.save()
        print('---------------')
        print(message_object)
        print('---------------')
       # message_object.feedbacks.add(new_feedback)
        serializer = FeedbackSerializer(new_feedback)
        return Response(serializer.data)



    



