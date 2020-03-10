from .models import ToDoItem, Course
from django.template.defaultfilters import mark_safe
from django.utils import timezone
from django import forms
from tempus_dominus.widgets import DateTimePicker #https://pypi.org/project/django-tempus-dominus/



class EditToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'duedate', 'location', 'recur_freq','end_recur_date', 'priority', 'category', 'course']
        labels = { 'recur_freq': mark_safe('Repeat'), 'end_recur_date': mark_safe('End repeat'), 'duedate' : mark_safe('Due Date'),} #label and bold it
        widgets = {'description': forms.Textarea(attrs={'cols': 35, 'rows': 3}),
                  'duedate': DateTimePicker(attrs={'placeholder': 'yyyy-mm-dd HH:MM',
                                                        'append': 'fa fa-calendar',
                                                        'icon_toggle': True,},
                                                 options={ 'useCurrent': True,
                                                           'collapse': True,}
                                                 ),
                   'end_recur_date': DateTimePicker(attrs={'placeholder': 'yyyy-mm-dd HH:MM',
                                                        'append': 'fa fa-calendar',
                                                        'icon_toggle': True,},
                                                 options={ 'useCurrent': True,
                                                           'collapse': True,}
                                                 ),
                  }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['course'].queryset = Course.objects.all()


class AddToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'duedate', 'location', 'recur_freq','end_recur_date', 'priority', 'category', 'course']
        labels = { 'recur_freq': mark_safe('Repeat'), 'end_recur_date': mark_safe('End repeat'), 'duedate' : mark_safe('Due Date'),} #label and bold it
        widgets = {'description': forms.Textarea(attrs={'cols': 35, 'rows': 3}),
                  'duedate': DateTimePicker(attrs={'placeholder': 'yyyy-mm-dd HH:MM',
                                                        'append': 'fa fa-calendar',
                                                        'icon_toggle': True,},
                                                 options={ 'useCurrent': True,
                                                           'collapse': True,}
                                                 ),
                   'end_recur_date': DateTimePicker(attrs={'placeholder': 'yyyy-mm-dd HH:MM',
                                                        'append': 'fa fa-calendar',
                                                        'icon_toggle': True,},
                                                 options={ 'useCurrent': True,
                                                           'collapse': True,}
                                                 ),
                  }

class AddCourseForm( forms.ModelForm ):
    class Meta:
        model = Course
        fields = ['course_name', 'course_abbrev', 'course_prof']

class EditCourseForm( forms.ModelForm ):
    class Meta:
        model = Course
        fields = ['course_name', 'course_abbrev', 'course_prof']