from django.contrib import admin
from .models import ToDoItem, Course, Extracurricular, Note


class ToDoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),

        ('Details', {'fields': ['description', 'duedate', 'location',
                                'priority', 'recur_freq', 'end_recur_date', 'completed']}),
    ]

    list_display = ('title', 'duedate', 'priority', 'recur_freq', 'completed')
    list_filter = ['duedate']
    search_fields = ['title']


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['course_name']}),

        ('Details',
         {'fields': ['course_abbrev', 'course_prof']}),
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


class NoteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'text']})
    ]
    list_display = ('user', 'text')
    list_filter = ['user']
    search_fields = ['text']


admin.site.register(ToDoItem, ToDoAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Extracurricular, ECAdmin)
admin.site.register(Note, NoteAdmin)
