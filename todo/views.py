from django.shortcuts import render

from .models import ToDoItem

# Create your views here.

class ToDoListView(generic.ListView):
    template_name = 'todo/index.html'
    context_object_name = 'todo_list'

    #This is how the tasks are gathered!