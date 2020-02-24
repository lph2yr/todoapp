from django import forms
from .models import ToDoItem
from django.template.defaultfilters import mark_safe
from django.utils import timezone
from datetime import timezone
from django import forms


class EditToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'duedate', 'location', 'recur_freq','end_recur_date', 'priority']
        labels = { 'recur_freq': mark_safe('Repeat'), 'end_recur_date': mark_safe('End repeat'), 'duedate' : mark_safe('Due Date'),} #label and bold it
        widgets = {'description': forms.Textarea(attrs={'cols': 35, 'rows': 5}),
                  'duedate': forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd HH:MM'}),
                   'end_recur_date': forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd HH:MM'})
                  }


class AddToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'duedate', 'location', 'recur_freq','end_recur_date', 'priority']
        labels = { 'recur_freq': mark_safe('Repeat'), 'end_recur_date': mark_safe('End repeat'), 'duedate' : mark_safe('Due Date'),} #label and bold it
        widgets = {'description': forms.Textarea(attrs={'cols': 35, 'rows': 5}),
                  'duedate': forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd HH:MM'}),
                   'end_recur_date': forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd HH:MM'}),
                  }

