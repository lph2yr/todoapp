import datetime
from django.db import models
from django.db.models import Model
from django.utils import timezone

# Create your models here.

class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=600, default="")
    duedate = models.DateTimeField()
    #date_added = models.DateTimeField()
    location = models.CharField(max_length=50)
    completed = models.BooleanField(default=False) 
    def __str__(self):
    	return self.title

    
