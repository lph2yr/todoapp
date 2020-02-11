from django.shortcuts import render

from .models import ToDoItem

# Create your views here.

class ToDoListView(generic.ListView):
    template_name = 'todo/todo_list.html'
    context_object_name = 'todo_list'

    #This is how the tasks are gathered!
    def get_queryset(self):
        return ToDoItem.objects().order_by(date)