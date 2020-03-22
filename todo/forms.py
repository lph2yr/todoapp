from .models import ToDoItem, Course, Extracurricular
from django.template.defaultfilters import mark_safe
from django.utils import timezone
from django import forms
from tempus_dominus.widgets import DateTimePicker, DatePicker #https://pypi.org/project/django-tempus-dominus/



class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'duedate', 'location', 'recur_freq','end_recur_date', 'priority', 'category', 'course', 'ec', 'progress']
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




class CourseForm( forms.ModelForm ):
    class Meta:
        model = Course
        fields = ['course_name', 'course_abbrev', 'course_prof']


class ECForm( forms.ModelForm ):
    class Meta:
        model = Extracurricular
        fields = ['name', 'detail', 'start_date', 'end_date', 'active']
        widgets = {
            'detail': forms.Textarea(attrs={'cols': 35, 'rows': 2}),
            'start_date': DatePicker(attrs={'placeholder': 'yyyy-mm-dd',
                                                        'append': 'fa fa-calendar',
                                                        'icon_toggle': True,},
                                                 options={ 'useCurrent': True,
                                                           'collapse': True,}
                                                 ),
            'end_date': DatePicker(attrs={'placeholder': 'yyyy-mm-dd',
                                            'append': 'fa fa-calendar',
                                            'icon_toggle': True, },
                                     options={'useCurrent': True,
                                              'collapse': True, }
                                     ),
        }


