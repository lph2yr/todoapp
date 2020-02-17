from django.contrib import admin

# Register your models here.
from .models import ToDoItem

class ToDoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Details', {'fields': [ 'description', 'duedate', 'location', 'completed', 'priority' ] }),
    ]

    list_display = ('title', 'duedate', 'completed')
    list_filter = ['duedate']
    search_fields = ['title']
    

admin.site.register(ToDoItem, ToDoAdmin )