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
        #customize day of week
        #every other day
        #every other week

    end_recur_date = models.DateTimeField()
    #end repeat date and time
    #end after a day
    #never
    #end after # occurrences

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

    def createRecurring(self, freq, recur_date, end_date ):
        # creating new To Do items with same title, description, location
        # changing due date; default false_completed
        recur_todo = self( title = self.title,
                           description = self.description,
                           location = self.location,
                           duedate = recur_date,
                           completed = False,
                           recur_freq = freq,
                           end_recur_date = end_date )
        #recur date = current due date + (daily = +1) or (weekly = + 7) or (monthly = ...) or (yearly = ....)
        return recur_todo
'''
ALGORITHM:
User -> edit 
Recur_freq -> list drop down --> choose --> update recur_freq field
    end_date appears --> if don't provide end_date --> error message
    if provide end_date --> change end_recur_date field
        #never --> have it end in 2500
        #after date --> change end_recur_date field
        #after # occurrences --> count occurences
    create object
'''
    
