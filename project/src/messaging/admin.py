from django.contrib import admin
from .models import Messages, Feedback, Topics

admin.site.register(Feedback)
admin.site.register(Topics)
admin.site.register(Messages)
