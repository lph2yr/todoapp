from .models import ToDoItem, Course, Extracurricular, SubTask
from django.template.defaultfilters import mark_safe
from django.utils import timezone
from django import forms
# https://pypi.org/project/django-tempus-dominus/
from tempus_dominus.widgets import DateTimePicker, DatePicker
import datetime
from datetime import date
from django.forms import modelformset_factory


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'duedate', 'location', 'recur_freq',
                  'end_recur_date', 'priority', 'category', 'course', 'ec', 'progress']
        labels = {'recur_freq': mark_safe('Repeat'), 'end_recur_date': mark_safe(
            'End repeat'), 'duedate': mark_safe('Due Date'), }  # label and bold it
        widgets = {'description': forms.Textarea(attrs={'cols': 35, 'rows': 5}),
                   'duedate': DateTimePicker(attrs={'placeholder': 'yyyy-mm-dd HH:MM',
                                                    'append': 'fa fa-calendar',
                                                    'icon_toggle': True, },
                                             options={'useCurrent': True,
                                                      'collapse': True, }
                                             ),
                   'end_recur_date': DateTimePicker(attrs={'placeholder': 'yyyy-mm-dd HH:MM',
                                                           'append': 'fa fa-calendar',
                                                           'icon_toggle': True, },
                                                    options={'useCurrent': True,
                                                             'collapse': True, }
                                                    ),
                   }

    def filter_course_and_ec(self, user=None):
        if user:
            self.fields['course'].queryset = Course.objects.filter(
                user=user)
            self.fields['ec'].queryset = Extracurricular.objects.filter(
                user=user)
        else:
            self.fields['course'].queryset = Course.objects.filter(
                user__isnull=True)
            self.fields['ec'].queryset = Extracurricular.objects.filter(
                user__isnull=True)


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['detail']


SubTaskModelFormSet = modelformset_factory(
    SubTask,
    fields=('detail',),
    extra=1,
    widgets={'detail': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Create subtasks here'
    })}
)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_abbrev', 'course_prof']


class ECForm(forms.ModelForm):
    class Meta:
        model = Extracurricular
        fields = ['name', 'detail', 'start_date', 'end_date', 'active']
        widgets = {
            'detail': forms.Textarea(attrs={'cols': 35, 'rows': 2}),
            'start_date': DatePicker(attrs={'placeholder': 'yyyy-mm-dd',
                                            'append': 'fa fa-calendar',
                                            'icon_toggle': True, },
                                     options={'useCurrent': True,
                                              'collapse': True, }
                                     ),
            'end_date': DatePicker(attrs={'placeholder': 'yyyy-mm-dd',
                                          'append': 'fa fa-calendar',
                                          'icon_toggle': True, },
                                   options={'useCurrent': True,
                                            'collapse': True, }
                                   ),
        }


class DayForm(forms.Form):
    date = forms.DateField(widget = DatePicker(attrs={'placeholder': 'yyyy-mm-dd',
                                          'append': 'fa fa-calendar',
                                          'icon_toggle': True, },
                                   options={'useCurrent': True,
                                            'collapse': True, }))

    def __str__(self):
        # https://stackoverflow.com/questions/19901410/django-how-to-get-value-from-charfield-and-modelchoicefield
        day = self.cleaned_data['date'].strftime("%d")
        month = self.cleaned_data['date'].strftime("%b")
        year = self.cleaned_data['date'].strftime("%Y")
        
        return "/day/" + year + "/" + month + "/" + day


class WeekForm(forms.Form):
    
    today = date.today()
    date = forms.DateField(widget = DatePicker(attrs={'placeholder': 'yyyy-mm-dd',
                                          'append': 'fa fa-calendar',
                                          'icon_toggle': True, },
                                   options={'useCurrent': True,
                                            'collapse': True, }))

    def __str__(self):
        #2020/week/17
        week = self.cleaned_data['date'].strftime("%W")
        year = self.cleaned_data['date'].strftime("%Y")
        
        return "/" + year + "/week/" + week


class MonthForm(forms.Form):
    JAN = 'Jan'
    FEB = 'Feb'
    MAR = 'Mar'
    APR = 'Apr'
    MAY = 'May'
    JUN = 'Jun'
    JUL = 'Jul'
    AUG = 'Aug'
    SEP = 'Sep'
    OCT = 'Oct'
    NOV = 'Nov'
    DEC = 'Dec'

    MONTH_CHOICES = [
        (JAN, 'Jan'),
        (FEB, 'Feb'),
        (MAR, 'Mar'),
        (APR, 'Apr'),
        (MAY, 'May'),
        (JUN, 'Jun'),
        (JUL, 'Jul'),
        (AUG, 'Aug'),
        (SEP, 'Sep'),
        (OCT, 'Oct'),
        (NOV, 'Nov'),
        (DEC, 'Dec'),
    ]
    month = forms.ChoiceField(choices=MONTH_CHOICES)
    year = forms.CharField(max_length=4)  # add default to be current year
    # returns the custom url for the redirect

    def __str__(self):
        # https://stackoverflow.com/questions/19901410/django-how-to-get-value-from-charfield-and-modelchoicefield
        return "/month/" + self.cleaned_data['year'] + "/" + self.cleaned_data['month']
