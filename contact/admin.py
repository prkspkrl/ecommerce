from django.contrib import admin

from .models import Contact, Socialmedia, Feedback
# Register your models here.
admin.site.register(Contact)
admin.site.register(Socialmedia)
admin.site.register(Feedback)