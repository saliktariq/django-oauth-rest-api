from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from messaging.views import MessagesViewset, FeedbackViewset, TopicsViewset, MessagesSortedByInteractionViewSet, SearchMessageByTopic, SearchExpiredMessageByTopic, SearchMessageByTopicSorted
from messaging.models import Messages, Feedback, Topics

#Defining default router
router = DefaultRouter()

##Registering messaging viewsets here to router
router.register('message', MessagesViewset, basename = 'Messages')
router.register('feedback', FeedbackViewset, basename = 'Feedback')
router.register('topic', TopicsViewset, basename = 'Topics')
router.register('sortedmessages', MessagesSortedByInteractionViewSet, basename = 'SortedMessages')
router.register('messagebytopic', SearchMessageByTopic, basename = 'MessageByTopic')
router.register('messagebytopicsorted', SearchMessageByTopicSorted, basename = 'MessageByTopicSorted')
router.register('expiredmessagebytopic', SearchExpiredMessageByTopic, basename = 'ExpiredMessageByTopic')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')), #setting IP:8000/o/ as URL resource to perform authentication
    path('authentication/', include('users.urls')), #TOKEN access/refresh/revoke token addresses are preceded by /authentication/
    path('v1/', include(router.urls)), #setting IP:8000/v1/ as the base address for version 1 of our rest API

]
