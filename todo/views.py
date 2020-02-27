from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import EditToDoForm, AddToDoForm
from .models import ToDoItem
from django.views.generic.edit import CreateView, UpdateView
from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta


class ToDoListView(generic.ListView):
    template_name = 'todo/todo_list.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        # update the priority twice a day if the due date is getting close
        # if datetime.datetime.utcnow().replace(tzinfo=timezone.utc).hour
        for item in ToDoItem.objects.all():
            timediff = (item.duedate - timezone.now()) / \
                datetime.timedelta(days=1)
            if timediff <= 1:
                item.priority = 'HI'
            elif timediff <= 2:
                item.priority = 'MD'
            else:
                item.priority = 'LO'
            item.save()
        return ToDoItem.objects.filter(completed=False).order_by('duedate')


class CompletedView(generic.ListView):
    template_name = 'todo/todo_list.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        return ToDoItem.objects.filter(completed=True).order_by('duedate')


# https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-editing/
class AddToDoItemView(CreateView):
    model = ToDoItem
    template_name = "todo/todoitem_form.html"
    form_class = AddToDoForm

    # overriding form_valid function to redirect to create recurrences when add a todo item
    def form_valid(self, form):
        self.object = form.save()
        if (self.object.recur_freq != 'NEVER'):
            return redirect('todo_list:create_recurrences', todo_item_id=self.object.id)
        else:
            self.object.save()
            return redirect('todo_list:todo_list')


class EditToDo(UpdateView):
    model = ToDoItem
    template_name = "todo/edit_todoitem_form.html"
    form_class = EditToDoForm


def delete_todo(request, todo_item_id):
    item = ToDoItem.objects.get(pk=todo_item_id)
    item.delete()
    return redirect('todo_list:todo_list')


def create_recurrences(request, todo_item_id):
    todo_item = get_object_or_404(ToDoItem, pk=todo_item_id)  # get obj

    # TODO: if recur_freq is changed to NEVER for a current item that's been set as repeated

    # if recur_freq is not NEVER
    if (todo_item.recur_freq != 'NEVER'):
        end_date = todo_item.end_recur_date  # get end_recur_date from current obj
        # find current_time --> may change to date_created!!!!!!!
        current_time = timezone.now()
        due_date = todo_item.duedate
        if (todo_item.recur_freq == 'DAILY'):
            delta = end_date - due_date  # find the time differences
            delta_day = delta.days + 1  # get the day dif of delta
            # loop thro delta_dif to create and save that many objects
            for i in range(1, delta_day + 1):
                ToDoItem.objects.create(
                    title=todo_item.title,
                    description=todo_item.description,
                    location=todo_item.location,
                    duedate=todo_item.duedate + relativedelta(days=+i),
                    recur_freq=todo_item.recur_freq,
                    end_recur_date=todo_item.end_recur_date,
                    priority=todo_item.priority
                    # completed = default False
                )

        elif (todo_item.recur_freq == 'WEEKLY'):
            delta = end_date - due_date  # find the time differences
            delta_day = delta.days
            weeks = delta_day // 7  # number of weeks
            for i in range(1, weeks + 1):
                ToDoItem.objects.create(
                    title=todo_item.title,
                    description=todo_item.description,
                    location=todo_item.location,
                    duedate=todo_item.duedate + relativedelta(weeks=+i),
                    recur_freq=todo_item.recur_freq,
                    end_recur_date=todo_item.end_recur_date,
                    priority=todo_item.priority
                    # completed = default False
                )

        elif (todo_item.recur_freq == 'MONTHLY'):
            delta = end_date - due_date  # find the time differences
            DAYS_IN_YR = 365
            MONTHS_IN_YR = 12
            DAYS_IN_MONTHS = 30  # roughly
            delta_month = (delta.days // DAYS_IN_YR) * MONTHS_IN_YR
            # days left that's not a year
            delta_remainders = (delta.days % DAYS_IN_YR)
            months_leftover = delta_remainders // DAYS_IN_MONTHS

            for i in range(1, delta_month + months_leftover + 1):
                ToDoItem.objects.create(
                    title=todo_item.title,
                    description=todo_item.description,
                    location=todo_item.location,
                    duedate=todo_item.duedate + relativedelta(months=+i),
                    recur_freq=todo_item.recur_freq,
                    end_recur_date=todo_item.end_recur_date,
                    priority=todo_item.priority
                    # completed = default False
                )
        elif (todo_item.recur_freq == 'YEARLY'):
            delta_year = end_date.year - due_date.year  # find the time differences
            # loop thro day_dif to create and save that many obj
            for i in range(1, delta_year + 1):
                ToDoItem.objects.create(
                    title=todo_item.title,
                    description=todo_item.description,
                    location=todo_item.location,
                    duedate=todo_item.duedate + relativedelta(years=+i),
                    recur_freq=todo_item.recur_freq,
                    end_recur_date=todo_item.end_recur_date,
                    priority=todo_item.priority
                    # completed = default False
                )

    return redirect('todo_list:todo_list')


def completeToDo(request, todo_item_id):
    # Todo item to be completed
    completedToDo = ToDoItem.objects.get(id=todo_item_id)
    completedToDo.completed = not completedToDo.completed
    completedToDo.save()

    return redirect('todo_list:todo_list')
