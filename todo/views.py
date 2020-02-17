from django.shortcuts import render, redirect
from django.views import generic
from .forms import ToDoForm
from .models import ToDoItem


# Create your views here.
class ToDoListView(generic.ListView):
    #the template this view uses
    template_name = 'todo/todo_list.html'
    #this is what the list with the todo_items is called
    context_object_name = 'todo_list'

    #This is how the tasks are gathered!
    def get_queryset(self):
        return ToDoItem.objects..filter(completed=False).order_by('-duedate')

#function processes input data of Date and Time and updates it in Database for todo_item at todo_item_id
#@param: request, todo_item_id
def detail( request, todo_item_id ):
    todo_item = ToDoItem.objects.get(id=todo_item_id) #get current todo_item with the id
    form = ToDoForm(request.POST) #get data from form
    if form.is_valid():
        #https://stackoverflow.com/questions/4706255/how-to-get-value-from-form-field-in-django-framework
        datetime = form['duedate'].value()
        todo_item.duedate = str(datetime) #datetime field is actually string; set the duedate field to the new date
        todo_item.save() #save todo_item
        form = ToDoForm() #reset blank form
    else:
        form = ToDoForm() #reset blank form
    context = {'todo_item': todo_item, 'form':form}
    return render(request, 'todo/detail.html', context)

#function changes a todo from incomplete to complete (completed = False -> True)
def completeToDo(request, todo_item_id):
    #Todo item to be completed
    completedToDo = ToDoItem.objects.get(id=todo_item_id)
    completedToDo.complete = True
    completedToDo.save()

    return redirect('todo_list:todo_list')

class CompletedView(generic.ListView):
    template_name = 'todo/completed.html'
    context_object_name = 'todo_list'
    def get_queryset(self):
        return ToDoItem.objects.filter(completed=True).order_by('duedate')
