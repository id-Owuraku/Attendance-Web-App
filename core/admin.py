from django.contrib import admin
from .models import Profile,Course,Class,Event

# Register your models here.
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Event)