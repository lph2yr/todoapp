from django.db import models
from django.db.models import Model
import django.utils
from model_utils import FieldTracker

# Create your models here.

class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=600, blank=True, default="")
    duedate = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    #date_created = models.DateTimeField(default=timezone.now()) #just added
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


    end_recur_date = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    #end repeat date and time
    #end after a specific day
    #never
    #end after # occurrences

    # priority choices
    HIGH = 'HI'
    MEDIUM = 'MD'
    LOW = 'LO'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High')
    ]
    priority = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        default=LOW,
    )

    #category choices
    CATEGORIES = [
        ('NN', 'None'),
        ('AC', 'Academics'),
        ('EC', 'Extracurriculars'),
        ('JB', 'Job'),
        ('SC', 'Social'),
        ('PS', 'Personal'),
        ('OT', 'Other')
    ]
    category = models.CharField(
        max_length=2,
        choices = CATEGORIES,
        default='NN',
        verbose_name='Category',
    )

    #tags???????????????????????????????

    tracker = FieldTracker() #track changes to fields

    def __str__(self):
    	return self.title + " " + self.duedate.strftime('%Y-%m-%d')

    def is_past_due(self):
        now = django.utils.timezone.now
        return now > self.duedate.date()

    def is_today_duedate(self):
        now = django.utils.timezone.now().replace(tzinfo=None)
        due = self.duedate.replace(tzinfo=None)
        delta = abs( now - due )
        day_dif = delta.days
        is_same = day_dif == 0
        return is_same

'''
class Course(models.Model):
    todo = models.ForeignKey(ToDoItem, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    
    def __str__(self):
        return self.title
'''