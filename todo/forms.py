from .models import ToDoItem, Course
from django.template.defaultfilters import mark_safe
from django.utils import timezone
from django import forms
from tempus_dominus.widgets import DateTimePicker #https://pypi.org/project/django-tempus-dominus/



class ToDoForm(forms.ModelForm):
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




class CourseForm( forms.ModelForm ):
    class Meta:
        model = Course
        fields = ['course_name', 'course_abbrev', 'course_prof']




class DayForm(forms.Form):
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
    month = forms.ChoiceField(choices = MONTH_CHOICES)
    day = forms.CharField(max_length = 2)
    year = forms.CharField(max_length = 4) #add default to be current year 
    #returns the custom url for the redirect
    def __str__(self):
        #https://stackoverflow.com/questions/19901410/django-how-to-get-value-from-charfield-and-modelchoicefield
        return "/day/" + self.cleaned_data['year'] + "/" + self.cleaned_data['month'] + "/" + self.cleaned_data['day']