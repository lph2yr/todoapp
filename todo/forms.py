from django import forms
from .models import ToDoItem
from django.template.defaultfilters import mark_safe
from django.utils import timezone


class EditToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'duedate','recur_freq','end_recur_date','duedate'] #only changing duedate for now
        widgets = {'duedate': forms.DateTimeInput(format='%YYYY-%mm-%dd %HH:%MM:%SS',
                                                  attrs={'type': 'datetime', 'placeholder':'yyyy-mm-dd HH:MM'})}
        #widget formatting a little funky right now. Fix later
        labels = { 'duedate' : mark_safe('<strong>Due Date </strong>'),} #label and bold it



class AddToDoForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=600)
    duedate = forms.DateTimeField()
    #date_added = models.DateTimeField()
    location = forms.CharField(max_length=50)

    #recurrence freq choices
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    YEARLY = 'YEARLY'
    FREQ_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (YEARLY, 'Yearly'),
    ]
    recur_freq = forms.CharField(
        max_length=7,
        choices=FREQ_CHOICES,
        default=DAILY,
    )
    end_recur_date = forms.DateTimeField(default=timezone.now, blank=True)

    # priority choices
    HIGH = 'HI'
    MEDIUM = 'MD'
    LOW = 'LO'
    PRIORITY_CHOICES = [
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    ]
    priority = forms.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        default=LOW,
    )