from django import forms
from .models import ToDoItem
from django.template.defaultfilters import mark_safe
from django.utils import timezone
from bootstrap_datepicker_plus import DateTimePickerInput #https://pypi.org/project/django-bootstrap-datepicker-plus/
from django import forms


class EditToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'duedate', 'location', 'recur_freq','end_recur_date', 'priority']
        widgets = { 'duedate': DateTimePickerInput(
            options={
                "format": "MM-DD-YYYY HH:MM",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            }
        ), }
        #widget formatting a little funky right now. Fix later
        labels = { 'recur_freq': mark_safe('Repeat'), 'end_recur_date': mark_safe('End repeat date'), 'duedate' : mark_safe('Due Date'),} #label and bold it



class AddToDoForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=600)
    duedate = forms.DateTimeField()
    #date_added = models.DateTimeField()
    location = forms.CharField(max_length=50)

    '''
    #recurrence freq choices
    NEVER = 'Never'
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
    '''

