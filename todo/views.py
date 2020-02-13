from django.shortcuts import render
from django.views import generic
from datetime import datetime

from .models import ToDoItem

# Create your views here.

class ToDoListView(generic.ListView):
    #the template this view uses
    template_name = 'todo/todo_list.html'
    #this is what the list with the todo items is called
    context_object_name = 'todo_list'

    #This is how the tasks are gathered!
    def get_queryset(self):
        return ToDoItem.objects.filter(completed=False).order_by('duedate')

class CompletedView(generic.ListView):
    template_name = 'todo/todo_list.html'
    context_object_name = 'todo_list'
    def get_queryset(self):
        return ToDoItem.objects.filter(completed=True).order_by('duedate')

