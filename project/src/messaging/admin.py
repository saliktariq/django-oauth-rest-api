from django.contrib import admin
from .models import Messages, Feedback, Topics

#Disable following registrations as depth=1 is being used for serializers 
#which would cause integrity constraint issue as it will not show related 
# forms on admin site while posting. That is, it wouldn't show Topics in Messages forms on admin panel

admin.site.register(Feedback)
admin.site.register(Topics)
admin.site.register(Messages)
