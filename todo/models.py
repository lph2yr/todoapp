from django.db import models
from django.db.models import Model
from django.utils import timezone

# Create your models here.

class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=600, blank=True, default="")
    duedate = models.DateTimeField(default=timezone.now(), blank=True)
    date_created = models.DateTimeField(default=timezone.now()) #just added
    location = models.CharField(max_length=50, blank=True)
    completed = models.BooleanField(default=False)

    #recurrence freq choices
    NEVER = 'NEVER'
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    YEARLY = 'YEARLY'
    FREQ_CHOICES = [
        (NEVER, 'Never'),
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (YEARLY, 'Yearly'),
    ]
    recur_freq = models.CharField(
        max_length=7,
        choices = FREQ_CHOICES,
        default = NEVER,
    )
        #customize day of week
        #every other day
        #every other week


    end_recur_date = models.DateTimeField(default=timezone.now(), blank=True)
    #end repeat date and time
    #end after a specific day
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
    	return self.title + " " + self.duedate.strftime('%Y-%m-%d')

    def is_past_due(self):
        now = timezone.now()
        return now > self.duedate.date()

    def is_today_duedate(self):
        now = timezone.now().replace(tzinfo=None)
        due = self.duedate.replace(tzinfo=None)
        delta = abs( now - due )
        day_dif = delta.days
        is_same = day_dif == 0
        return is_same

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
    
