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
        widgets = {
            'duedate': DateTimePickerInput(
                attrs={'class': 'datetimepicker'},
                options={
                    "format": "YYYY-MM-DD HH:MM",
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                },
                ),
            'end_recur_date': DateTimePickerInput(
                attrs={'class': 'datetimepicker'},
                options={
                    "format": "YYYY-MM-DD HH:MM",
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                },
            ),

        }
        labels = { 'recur_freq': mark_safe('Repeat'), 'end_recur_date': mark_safe('End repeat'), 'duedate' : mark_safe('Due Date'),} #label and bold it



class AddToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'duedate', 'location', 'recur_freq','end_recur_date', 'priority']
        widgets = {
            'duedate': DateTimePickerInput(
                attrs={'class': 'datetimepicker'},
                options={
                    "format": "YYYY-MM-DD HH:MM",
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                },
                ),
            'end_recur_date': DateTimePickerInput(
                attrs={'class': 'datetimepicker'},
                options={
                    "format": "YYYY-MM-DD HH:MM",
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                },
            ),
        }
        labels = { 'recur_freq': mark_safe('Repeat'), 'end_recur_date': mark_safe('End repeat'), 'duedate' : mark_safe('Due Date'),} #label and bold it


