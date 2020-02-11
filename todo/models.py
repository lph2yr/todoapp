import datetime
from django.db import models
from django.db.models import Model
from django.utils import timezone

# Create your models here.

class toDoItem(models.Model):
    title = models.CharField(max_length=100)
    time = models.DateTimeField()
    date = models.DateField()
    location = models.CharField(max_length=50)
    completed = models.BooleanField(default=False) 
    def __str__(self):
    	return self.title

    
