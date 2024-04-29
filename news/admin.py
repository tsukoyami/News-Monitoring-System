from django.contrib import admin
from .models import Company, registeredUsers, Subscriber, Source, Story

# Register your models here.
admin.site.register(Company)
admin.site.register(registeredUsers)
admin.site.register(Subscriber)
admin.site.register(Source)
admin.site.register(Story)
