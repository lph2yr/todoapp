from django import forms
from .models import ToDoItem
from django.template.defaultfilters import mark_safe


class EditToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['duedate'] #only changing duedate for now
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