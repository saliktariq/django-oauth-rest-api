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

"""
This viewset serves the endpoint /v1/message. If no post_identifier number is provided, it fetches all records.
"""
class MessagesViewset(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer

    def get_queryset(self):
        messages = Messages.objects.all()
        return messages

    #If post_identifier number is provided, it fetches specific post eg., /v1/message/1/
    #Learnt by following https://www.youtube.com/watch?v=ws0jwg1J0BU&list=PLmDLs7JbXWNjr5vyJhfGu69sowgIUl8z5&index=12
    def retrieve(self, request, *args, **kwargs): 

        #retrieving kwargs into parameter variable
        parameters = kwargs
        #Using try/except so that if an unknown key is provided, exceptions can be handled properly
        try:
            message = Messages.objects.get(post_identifier = parameters['pk'])
            serializer = MessagesSerializer(message) # use extra argument many=True if expecting multiple records
            return Response(serializer.data)
        #Ref: https://stackoverflow.com/questions/52575523/how-to-capture-the-model-doesnotexist-exception-in-django-rest-framework
        except ObjectDoesNotExist:
            raise Http404 

    #Learnt by following https://www.youtube.com/watch?v=4dPVywV-X84&list=PLmDLs7JbXWNjr5vyJhfGu69sowgIUl8z5&index=14
    def create(self, request, *args, **kwargs):
        #Retrieving request data into message_data variable
        message_data = request.data
        #Accessing expiry_in_seconds field value and assigning it to variable value
        value = message_data['expiry_in_seconds']
        #Checking if expiry_in_seconds is not negative or zero
        if value <= 0:
            #Sending error response back for value less than or equal to zero
            return Response({
                'Error': 'Enter a positive expiry time delta in seconds.'
            })
        #calculating expired_time by adding expiry time to timezone.now() which is also creation_timestamp value
        expired_time_calculated = timezone.now() + timedelta(seconds = message_data['expiry_in_seconds'])

        #Creating Messages object
        new_message = Messages.objects.create(title=message_data['title'], message= message_data['message'],  expiry_in_seconds= expired_time_calculated, username= request.user.username)
        #Saving Messages object before assinging related field (Topics) to it.
        new_message.save()

        #As there can be more than one topics per post, looping through all topic values
        for topic in message_data['topic']:

            topic_object = Topics.objects.get(topic_name = topic['topic_name'])
            #Adding topic values to Message object
            new_message.topic.add(topic_object)
        #Serialising new Message object
        serializer = MessagesSerializer(new_message)
        #Returning response
        return Response(serializer.data)


"""
This viewset serves the endpoint /v1/topic. If no topic_name is provided, it fetches all records, otherwise fetch specific topic 
For example, to fetch all Tech topics, endpoint would be /v1/topic/T/
This retrieval per topic name functionality is redundant in the app  except for creating new topics and I only wrote it so it can be used in future where all 
posts per topic can be retrieved through this 
relation Topics -> Messages
"""
class TopicsViewset(viewsets.ModelViewSet):
    serializer_class = TopicsSerializer

    def get_queryset(self):
        topics = Topics.objects.all()
        return topics

    #Retrieve method to deal with specific topic query based on topic_name
    def retrieve(self, request, *args, **kwargs): 
        parameters = kwargs
        try:
            topic = Topics.objects.get(topic_name = parameters['pk'].upper()) #Making sure lowercase query value is converted to uppercase automatically
            serializer = TopicsSerializer(topic)
            return Response(serializer.data)

        except ObjectDoesNotExist:
            raise Http404

    #Function to create an object/record of Topics class and save it.
    def create(self, request, *args, **kwargs):
        topic_data = request.data
        new_topic = Topics.objects.create(topic_name=topic_data['topic_name'])
        new_topic.save()

        serializer = TopicsSerializer(new_topic)
        return Response(serializer.data)

"""
This viewset serves the endpoint /v1/feedback. If no id number is provided, it fetches all feedbacks.
"""

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
        #Retrieving related Message object from post_identifier field that relates Feedback to Messages
        message_object = Messages.objects.filter(post_identifier=feedback_data['post_identifier']).first()

        #Checking if the user entering feedback is not the same who is owner of Message object
        if (request.user.username == message_object.username):
            #Sending error in case Feedback object user is equal to Message object user
            return Response(
                {
                    "Error: ": "Can not give feedback on own post"
                }
            )


        #Checking if Message is not expired by comparing current time with message expiry
        if(timezone.now() > message_object.expiry_in_seconds):
            return Response(
                {
                    "Error: ": "Post is expired now, can not add comments."
                }
            )
        #Making sure a user does not like and dislike a post at the same time
        #this is an additional constraint that I have added to the Piazza app.
        if (feedback_data['is_liked'] and feedback_data['is_disliked']):
            return Response(
                {
                    "Error: ": "Post can not be liked and disliked at the same time."
                }
            )
        
        if(feedback_data['is_liked']):
            #If message is liked, update the likes counter on the Message object
            message_object.likes = message_object.likes + 1 #REF01
        else:
            message_object.likes = message_object.likes
        if(feedback_data['is_disliked']):
            #If message is dislikeed, update the disliked counter on the Message object
            message_object.dislikes = message_object.dislikes + 1 #REF01
        else:
            message_object.dislikes = message_object.dislikes
        #IMPORTANT: Coursework requirement says that most active post is the one that has most likes and dislikes,
        #I have changed the scope of 'active post' slightly by including the number of times a user commented on post as well
        #In order to change this back to strict coursework requirement, the following line may be moves under #REF01 AND #REF02
        message_object.total_interactions = message_object.total_interactions + 1
        #Saving feedback interaction values on Messages object
        message_object.save(update_fields=['likes', 'dislikes', 'total_interactions'])
        #Creating new feedback object
        new_feedback = Feedback.objects.create(is_liked= feedback_data['is_liked'],is_disliked= feedback_data['is_disliked'], comment= feedback_data['comment'], username= request.user.username, message=message_object)
        #Saving feedback
        new_feedback.save()

        #Serializing the Feedback object and returning to requester
        serializer = FeedbackSerializer(new_feedback)
        return Response(serializer.data)

"""
This viewset serves the endpoint /v1/sortedmessages. This would return messages from ALL topics sorted in order of most interacted message to
least interacted message. This endpoint is redundant at this point and not used as out of scope of coursework requirements
"""
class MessagesSortedByInteractionViewSet(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer

    def get_queryset(self):
        messages = Messages.objects.order_by('-total_interactions')
        return messages

"""
This viewset serves the endpoint /v1/messagebytopicsorted/{topic_name}. It facilitates searching messages by Topic in sorted in order of most interacted message to
least interacted message in the particular topic provided. Not providing any topic name to endpoint would render all messages. This is kept to minimise errors 
in case no topic_name is provided.
"""
class SearchMessageByTopicSorted(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer

    def get_queryset(self):
        messages = Messages.objects.all()
        return messages



    def retrieve(self, request, *args, **kwargs): 
        parameters = kwargs

        try:
            #icontains searches the given keyword in topic_name field and order_by orders the records high to low due to minus sign before total_interactions field.
            message = Messages.objects.filter(topic__topic_name__icontains = parameters['pk']).order_by('-total_interactions')
            serializer = MessagesSerializer(message, many=True) #many=True as multiple records are expected
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise Http404 

"""
This viewset serves the endpoint /v1/messagebytopic/{topic_name}. It facilitates searching messages by Topic in unsorted order for the particular topic provided. 
Not providing any topic name to endpoint would render all messages. This is kept to minimise errors in case no topic_name is provided.
"""
class SearchMessageByTopic(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer

    def get_queryset(self):
        messages = Messages.objects.all()
        return messages



    def retrieve(self, request, *args, **kwargs): 
        parameters = kwargs

        try:
            #icontains searches the given keyword in topic_name field
            message = Messages.objects.filter(topic__topic_name__icontains = parameters['pk'])
            serializer = MessagesSerializer(message, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise Http404 

"""
This viewset serves the endpoint /v1/expiredmessagebytopic/{topic_name}. As name suggests, it only returns expired messages in a given topic_name.
"""
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
            #Using dictionary to create returned object as I am utilising live_status field which is not a Model field but a serializer field and hence can not 
            #be used in the filter function.
            d= {}
            i = 1
            #Iterating through all messages and adding messages to dictionary that are expired, flagged by label live_status = False
            for msg in retrieved_messages:
                
                if not msg["live_status"]:
                    key_name = 'Expired message number: ' + str(i)
                    d[key_name] = msg
                i = i + 1
            #Returning dictionary in response
            return Response(d)
        except ObjectDoesNotExist:
            raise Http404 