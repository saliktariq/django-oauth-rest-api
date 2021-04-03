from rest_framework import viewsets
from .serializers import MessagesSerializer, FeedbackSerializer, TopicsSerializer
from .models import Messages, Feedback, Topics
from django.contrib.auth.models import User
from rest_framework.response import Response
from datetime import timedelta
import datetime
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class MessagesViewset(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer

    

    def get_queryset(self):
        messages = Messages.objects.all()
        return messages

    #Learnt by following https://www.youtube.com/watch?v=ws0jwg1J0BU&list=PLmDLs7JbXWNjr5vyJhfGu69sowgIUl8z5&index=12
    def retrieve(self, request, *args, **kwargs): 
        parameters = kwargs
        try:
            message = Messages.objects.get(post_identifier = parameters['pk'])
            serializer = MessagesSerializer(message) # use extra argument many=True if expecting multiple records
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise Http404 #https://stackoverflow.com/questions/52575523/how-to-capture-the-model-doesnotexist-exception-in-django-rest-framework

    #Learnt by following https://www.youtube.com/watch?v=4dPVywV-X84&list=PLmDLs7JbXWNjr5vyJhfGu69sowgIUl8z5&index=14
    def create(self, request, *args, **kwargs):
        message_data = request.data
        value = message_data['expiry_in_seconds']
        if value <= 0:
            return Response({
                'Error': 'Enter a positive expiry time delta in seconds.'
            })
        expired_time_calculated = timezone.now() + timedelta(seconds = message_data['expiry_in_seconds'])

        new_message = Messages.objects.create(title=message_data['title'], message= message_data['message'],  expiry_in_seconds= expired_time_calculated, username= request.user.username)
        
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
        try:
            topic = Topics.objects.get(topic_name = parameters['pk'].upper())
            serializer = TopicsSerializer(topic)
            return Response(serializer.data)

        except ObjectDoesNotExist:
            raise Http404


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
        try:
            feedback = Feedback.objects.get(id = parameters['pk'])
            serializer = FeedbackSerializer(feedback)
            return Response(serializer.data)

        except ObjectDoesNotExist:
            raise Http404



    def create(self, request, *args, **kwargs):
        feedback_data = request.data
        message_object = Messages.objects.filter(post_identifier=feedback_data['post_identifier']).first()


        if (request.user.username == message_object.username):
            return Response(
                {
                    "Error: ": "Can not give feedback on own post"
                }
            )



        if(timezone.now() > message_object.expiry_in_seconds):
            return Response(
                {
                    "Error: ": "Post is expired now, can not add comments."
                }
            )

        if (feedback_data['is_liked'] and feedback_data['is_disliked']):
            return Response(
                {
                    "Error: ": "Post can not be liked and disliked at the same time."
                }
            )
        

        if(feedback_data['is_liked']):
            message_object.likes = message_object.likes + 1
        else:
            message_object.likes = message_object.likes
        if(feedback_data['is_disliked']):
            message_object.dislikes = message_object.dislikes + 1
        else:
            message_object.dislikes = message_object.dislikes
        message_object.total_interactions = message_object.total_interactions + 1

        message_object.save(update_fields=['likes', 'dislikes', 'total_interactions'])


        new_feedback = Feedback.objects.create(is_liked= feedback_data['is_liked'],is_disliked= feedback_data['is_disliked'], comment= feedback_data['comment'], username= request.user.username, message=message_object)
        new_feedback.save()


        serializer = FeedbackSerializer(new_feedback)
        return Response(serializer.data)


class MessagesSortedByInteractionViewSet(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer

    def get_queryset(self):
        messages = Messages.objects.order_by('-total_interactions')
        return messages



class SearchMessageByTopic(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer

    def get_queryset(self):
        messages = Messages.objects.all()
        return messages



    def retrieve(self, request, *args, **kwargs): 
        parameters = kwargs

        try:
            message = Messages.objects.filter(topic__topic_name__icontains = parameters['pk']).order_by('-total_interactions')
            serializer = MessagesSerializer(message, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise Http404 

class SearchExpiredMessageByTopic(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer

    def get_queryset(self):
        messages = Messages.objects.all()
        return messages



    def retrieve(self, request, *args, **kwargs): 
        parameters = kwargs

        try:
            message = Messages.objects.filter(topic__topic_name__icontains = parameters['pk'])

            serializer = MessagesSerializer(message, many=True)
            retrieved_messages = serializer.data
            d= {}
            i = 1
            for msg in retrieved_messages:
                
                if not msg["live_status"]:
                    key_name = 'Expired message number: ' + str(i)
                    d[key_name] = msg
                i = i + 1
            
            return Response(d)
        except ObjectDoesNotExist:
            raise Http404 