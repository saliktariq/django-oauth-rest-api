from django.contrib import admin
from .models import Messages, Feedback, Topics

#Disable following registrations as I am using depth=1 for serializers 
#which would cause integrity constraint issue as it will not show related 
# forms on admin site while posting

admin.site.register(Feedback)
admin.site.register(Topics)
admin.site.register(Messages)
