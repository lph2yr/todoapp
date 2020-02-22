from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import EditToDoForm, AddToDoForm
from .models import ToDoItem
from django.views.generic.edit import CreateView, UpdateView

# Create your views here.
class ToDoListView(generic.ListView):
    #the template this view uses
    template_name = 'todo/todo_list.html'
    #this is what the list with the todo_items is called
    context_object_name = 'todo_list'

    #This is how the tasks are gathered!
    def get_queryset(self):
        return ToDoItem.objects.filter(completed=False).order_by('-duedate')
#Edit todo: function processes input data of Date and Time and updates it in Database for todo_item at todo_item_id

#https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-editing/

class AddToDoItemView(CreateView):
    model = ToDoItem
    template_name = "todo/todoitem_form.html"
    form_class = AddToDoForm
    #fields = ['title', 'description', 'duedate', 'location', 'recur_freq', 'end_recur_date', 'priority']


#function processes input data of Date and Time and updates it in Database for todo_item at todo_item_id
class EditToDo(UpdateView):
    model = ToDoItem
    template_name = "todo/edit_todoitem_form.html"
    form_class = EditToDoForm
    #new fields (recur_freq, end_recur_date) don't create new obj yet!!!

#function changes a todo from incomplete to complete (completed = False -> True)
def completeToDo(request, todo_item_id):
    #Todo item to be completed
    completedToDo = ToDoItem.objects.get(id=todo_item_id)
    completedToDo.completed = not completedToDo.completed
    completedToDo.save()

    return redirect('todo_list:todo_list')

class CompletedView(generic.ListView):
    template_name = 'todo/completed.html'
    context_object_name = 'todo_list'
    def get_queryset(self):
        return ToDoItem.objects.filter(completed=True).order_by('duedate')









'''
#@param: request, todo_item_id
def detail( request, todo_item_id ):
    todo_item = ToDoItem.objects.get(pk=todo_item_id) #get current todo_item with the id
    form = EditToDoForm(request.POST) #get data from form
    if form.is_valid():
        #https://stackoverflow.com/questions/4706255/how-to-get-value-from-form-field-in-django-framework
        new_title = form['title'].value()
        if (new_title != None ):
            todo_item.title = str(new_title)

        new_description = form['description'].value()
        if (new_description != None):
            todo_item.description = str(new_description)

        new_date = form['duedate'].value()
        if (new_date != None):
            todo_item.duedate = str(new_date) #datetime field is actually string; set the duedate field to the new date

        new_location = form['location'].value()
        if (new_location != None):
            todo_item.location = str(new_location)


        #new_freq = form[ 'recur_freq' ].value()
        #todo_item.recur_freq = str(new_freq)

        #new_end_date = form[ 'end_recur_date' ].value()
        #todo_item.end_recur_date = str(new_end_date).value()
        
        #new_priority = form ['priority'].value()
        #....

        todo_item.save() #save todo_item
        form = EditToDoForm() #reset blank form
    else:
        form = EditToDoForm() #reset blank form
    context = { 'todo_item': todo_item, 'form':form, }
    return render(request, 'todo/edit_todoitem_form.html', context)
'''

