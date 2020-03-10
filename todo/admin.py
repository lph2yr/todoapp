from django.contrib import admin

# Register your models here.
from .models import ToDoItem, Course

class ToDoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),

        ('Details', {'fields': [ 'description', 'duedate', 'location', 'priority', 'recur_freq', 'end_recur_date', 'completed' ] }),
    ]

    list_display = ('title', 'duedate', 'priority','recur_freq', 'completed')
    list_filter = ['duedate']
    search_fields = ['title']
    

class CourseAdmin( admin.ModelAdmin ):
    fieldsets = [
        (None,                {'fields': ['course_name']}),
        ('Details', {'fields': ['course_abbrev', 'course_prof']}        ),
    ]

    list_display = ('course_name', 'course_abbrev', 'course_prof')
    search_fields = ['course_name']

admin.site.register(ToDoItem, ToDoAdmin )
admin.site.register( Course, CourseAdmin )
