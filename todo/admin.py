from django.contrib import admin

# Register your models here.


from .models import ToDoItem, Course

class ToDoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),

        ('Details', {'fields': [ 'description', 'duedate', 'location', 'priority', 'recur_freq', 'end_recur_date', 'completed', 'category', 'course' ] }),
    ]

    list_display = ('title', 'duedate', 'priority','recur_freq', 'completed', 'category')
    list_filter = ['duedate']
    search_fields = ['title']

admin.site.register(ToDoItem, ToDoAdmin )

class CourseAdmin( admin.ModelAdmin ):
    fieldsets = [
        (None, {'fields': ['course_name']}),

        ('Details',
         {'fields': ['course_abbrev', 'cousre_prof']}),
    ]

    list_display = ('course_name', 'course_abbrev', 'course_prof')
    list_filter = ['course_name']
    search_fields = ['course_name']

admin.site.register( Course, CourseAdmin )
