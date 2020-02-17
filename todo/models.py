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
    recur_freq = models.TextField(max_length=7)
        #daily, weekly, monthly, yearly
    end_recur_date = models.DateTimeField()
    #end repeat date and time

    def __str__(self):
    	return self.title

    def createToDo(self, recur_date, false_completed, freq, end_date ):
        # creating new To Do items with same title, description, location
        recur_todo = self( title = self.title,
                           description = self.description,
                           location = self.location,
                           duedate = recur_date,
                           completed = false_completed,
                           recur_freq = freq,
                           end_recur_date = end_date )
        #changing due date; default false_completed
        return recur_todo
'''
ALGORITHM:
User -> edit 
Recur -> list drop down
    end_date appears --> if don't provide end_date --> error message
    if provide end_date
    
'''
    
