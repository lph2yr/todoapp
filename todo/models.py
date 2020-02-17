import datetime
from django.db import models
from django.db.models import Model
from django.utils import timezone

# Create your models here.

class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=600, blank=True, default="")
    duedate = models.DateTimeField()
    #date_added = models.DateTimeField()
    location = models.CharField(max_length=50, blank=True)
    completed = models.BooleanField(default=False)
    
    # priority choices
    HIGH = 'HI'
    MEDIUM = 'MD'
    LOW = 'LO'
    PRIORITY_CHOICES = [
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    ]
    priority = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        default=LOW,
    )
    def __str__(self):
    	return self.title

    
