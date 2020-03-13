from .models import ToDoItem, Specific, Category
from django.template.defaultfilters import mark_safe
from django.utils import timezone
from django import forms
from tempus_dominus.widgets import DateTimePicker #https://pypi.org/project/django-tempus-dominus/



class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'duedate', 'location', 'recur_freq','end_recur_date', 'priority', 'category', 'specific']
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
            self.fields['specific'].queryset = Specific.objects.none()

            '''
            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['specific'].queryset = Specific.objects.filter(category_id=category_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty Specific queryset
            elif self.instance.pk:
                self.fields['specific'].queryset = self.instance.category.specific_set.order_by('name')
            '''


class CategoryForm( forms.ModelForm ):
    class Meta:
        model = Category
        fields = ['cat']

class SpecificForm( forms.ModelForm ):
    class Meta:
        model = Specific
        fields = ['category', 'name', 'detail']



