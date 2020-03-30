from django.contrib import admin

# Register your models here.


from .models import ToDoItem, Course, Extracurricular

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
        (None, {'fields': ['course_name']}),

        ('Details',
         {'fields': ['course_abbrev', 'cousre_prof']}),
    ]

    list_display = ('course_name', 'course_abbrev', 'course_prof')
    list_filter = ['course_name']
    search_fields = ['course_name']

class ECAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Details',
         {'fields': ['detail', 'start_date', 'end_date', 'active']}),
    ]
    list_display = ('name', 'active')
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(ToDoItem, ToDoAdmin )
admin.site.register( Course, CourseAdmin )
admin.site.register( Extracurricular, ECAdmin )