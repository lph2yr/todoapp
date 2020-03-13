from django.contrib import admin

# Register your models here.


from .models import ToDoItem, Specific, Category

class ToDoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),

        ('Details', {'fields': [ 'description', 'duedate', 'location', 'priority', 'recur_freq', 'end_recur_date', 'completed' ] }),
    ]

    list_display = ('title', 'duedate', 'priority','recur_freq', 'completed')
    list_filter = ['duedate']
    search_fields = ['title']
    
class SpecificAdmin( admin.ModelAdmin ):
    fieldsets = [
        (None, {'fields': ['name']}),

        ('Details',
         {'fields': ['detail', 'category']}),
    ]

    list_display = ('name', 'category')
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(ToDoItem, ToDoAdmin )
admin.site.register( Specific, SpecificAdmin )

