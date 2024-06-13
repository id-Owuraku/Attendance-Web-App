from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django_google_maps.fields import AddressField, GeoLocationField  
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
  
    
    
    def __str__(self):
        return self.user.username

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    lecturer_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)

    def __str__(self):
        return self.class_name    

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_url=models.URLField(null=True)
    related_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location_address = models.CharField(max_length=200,null=True, blank=True)
    geolocation = GeoLocationField(max_length=100,null=True, blank=True)
    radius = models.DecimalField(max_digits=5, decimal_places=2)
    is_student_id_required = models.BooleanField(default=False)
    is_index_number_required = models.BooleanField(default=False)
    is_student_name_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    checkpoint_lat = models.DecimalField(decimal_places=7, max_digits=15, null=True)
    checkpoint_lng =  models.DecimalField(decimal_places=7, max_digits=15, null=True) 
    def __str__(self):
        if self.event_name:
            return self.event_name
        else:
            return f"Event ID: {self.event_id}" 
    
    class Meta:
        ordering = ['-created_at']

    
class CheckIn(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=100, blank=True, null=True)
    index_number = models.CharField(max_length=100, blank=True, null=True)
    student_name = models.CharField(max_length=100, blank=True, null=True)
    check_in_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CheckIn for {self.event}"    