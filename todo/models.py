from django.db import models
import django.utils
from model_utils import FieldTracker
import datetime

# Create your models here.


class Course(models.Model):
    course_name = models.CharField(max_length=50, verbose_name='Course Name')
    course_abbrev = models.CharField(max_length=10, verbose_name='Course Abbreviation')
    course_prof = models.CharField(max_length=20, verbose_name='Course Professor')

    def __str__(self):
        return self.course_name

class Extracurricular(models.Model):
    name = models.CharField(max_length=20, verbose_name="Name")
    detail = models.CharField(max_length=100, verbose_name='Details')
    start_date = models.DateField(default= datetime.date.today, blank=True, verbose_name='Start date')
    end_date = models.DateField( default= datetime.date.today, blank=True, verbose_name='End date')
    active = models.BooleanField( default = True )

    def __str__(self):
        return self.name


class ToDoItem(models.Model):
    course = models.ForeignKey( Course, on_delete=models.SET_NULL, null=True)
    ec = models.ForeignKey( Extracurricular, on_delete=models.SET_NULL, null=True, verbose_name='Extracurriculars')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=600, blank=True, default="")
    duedate = models.DateTimeField(default=django.utils.timezone.now, blank=True)
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

    has_title_changed = models.BooleanField(default=False)
    has_description_changed = models.BooleanField(default=False)
    has_duedate_changed = models.BooleanField(default=False)
    has_location_changed = models.BooleanField(default=False)
    has_recur_freq_changed = models.BooleanField(default=False)
    has_end_recur_date_changed = models.BooleanField(default=False)
    has_category_changed = models.BooleanField(default=False)
    has_priority_changed = models.BooleanField(default=False)

    count_future_events = models.IntegerField(default=1)

    tracker = FieldTracker() #track changes to fields

    def __str__(self):
       return self.title + " " + self.duedate.strftime('%Y-%m-%d') + " id: " + str(self.id)

    def is_past_due(self):
        now = django.utils.timezone.now
        return now > self.duedate.date()

    def is_today_duedate(self):
        now = django.utils.timezone.now()
        due = self.duedate
        is_same = now.day == due.day
        return is_same


#https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
