from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import ToDoForm, CourseForm
from .models import ToDoItem, Course
from django.views.generic.edit import CreateView, UpdateView
from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta


######################## TO DO view ################################
# https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-editing/
# allows adding new obj to database
class AddToDoItemView(CreateView):
    model = ToDoItem
    template_name = "todo/todoitem_form.html"
    form_class = ToDoForm

    # set title and duedate fields to be required
    def get_form(self, form_class=None):
        form = super(AddToDoItemView, self).get_form(form_class)
        form.fields['title'].required = True
        form.fields['duedate'].required = True
        form.fields['course'].required = False
        return form

    # overriding form_valid function to redirect to create_recurrences when add a todo item
    def form_valid(self, form):
        self.object = form.save()
        if (self.object.recur_freq != 'NEVER'):
            return redirect('todo_list:create_recurrences', todo_item_id=self.object.id)
        else:
            self.object.save()
            return redirect('todo_list:todo_list')


# function create recurrence of newly added objects based on recur_freq and end_recur_date fields
def create_recurrences(request, todo_item_id):
    # if recur_freq is not NEVER
    todo_item = get_object_or_404(ToDoItem, pk=todo_item_id)  # get obj
    # if recur_freq is not NEVER
    if (todo_item.recur_freq != 'NEVER'):
        end_date = todo_item.end_recur_date  # get end_recur_date from current obj
        due_date = todo_item.duedate  # get current duedate
        if (todo_item.recur_freq == 'DAILY'):
            # find the time differences
            delta = end_date - (due_date + relativedelta(days=+1))
            delta_day = delta.days + 1
            for i in range(1, delta_day + 1):
                ToDoItem.objects.create(
                    course=todo_item.course,
                    title=todo_item.title,
                    description=todo_item.description,
                    location=todo_item.location,
                    duedate=todo_item.duedate + relativedelta(days=+i),
                    recur_freq=todo_item.recur_freq,
                    end_recur_date=todo_item.end_recur_date,
                    priority=todo_item.priority,
                    category=todo_item.category
                    # completed = default False
                )

        elif (todo_item.recur_freq == 'WEEKLY'):
            delta = end_date - due_date  # find the time differences
            delta_day = delta.days
            weeks = delta_day // 7  # number of weeks
            for i in range(1, weeks + 1):
                ToDoItem.objects.create(
                    course=todo_item.course,
                    title=todo_item.title,
                    description=todo_item.description,
                    location=todo_item.location,
                    duedate=todo_item.duedate + relativedelta(weeks=+i),
                    recur_freq=todo_item.recur_freq,
                    end_recur_date=todo_item.end_recur_date,
                    priority=todo_item.priority,
                    category=todo_item.category
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
                    course=todo_item.course,
                    title=todo_item.title,
                    description=todo_item.description,
                    location=todo_item.location,
                    duedate=todo_item.duedate + relativedelta(months=+i),
                    recur_freq=todo_item.recur_freq,
                    end_recur_date=todo_item.end_recur_date,
                    priority=todo_item.priority,
                    category=todo_item.category,
                    # completed = default False
                )

        elif (todo_item.recur_freq == 'YEARLY'):
            delta_year = end_date.year - due_date.year  # find the time differences
            # loop thro day_dif to create and save that many obj
            for i in range(1, delta_year + 1):
                ToDoItem.objects.create(
                    course=todo_item.course,
                    title=todo_item.title,
                    description=todo_item.description,
                    location=todo_item.location,
                    duedate=todo_item.duedate + relativedelta(years=+i),
                    recur_freq=todo_item.recur_freq,
                    end_recur_date=todo_item.end_recur_date,
                    priority=todo_item.priority,
                    category=todo_item.category,
                    # completed = default False
                )
    return redirect('todo_list:todo_list')


# TODO: put in no changes made???????????????????????????????????
# view allows update/edit of object in database
class EditToDo(UpdateView):
    model = ToDoItem
    template_name = "todo/edit_todoitem_form.html"
    form_class = ToDoForm

    # set title and duedate fields to be required
    def get_form(self, form_class=None):
        form = super(EditToDo, self).get_form(form_class)
        form.fields['title'].required = True
        form.fields['duedate'].required = True
        form.fields['course'].required = False
        return form

    # override form_valid to check to see if recur_freq has changed
    # https://django-model-utils.readthedocs.io/en/latest/utilities.html#field-tracker
    def form_valid(self, form):
        todo = form.save(commit=False)
        if (self.request.POST.get("change-once")):  # only change fields for one instance
            todo.save()
            form.save_m2m()
            return redirect('todo_list:todo_list')
        elif (self.request.POST.get("change-all")):  # if changed for all future events and current instance
            fields_changed = self.object.tracker.changed()
            if (len(fields_changed) == 0):
                todo.save()
                form.save_m2m()
                return redirect('todo_list:todo_list')
            else:
                # TODO: how to track course changes?????????/
                todo.has_title_changed = self.object.tracker.has_changed('title')
                todo.has_description_changed = self.object.tracker.has_changed('description')
                todo.has_location_changed = self.object.tracker.has_changed('location')
                todo.has_category_changed = self.object.tracker.has_changed('category')
                todo.has_priority_changed = self.object.tracker.has_changed('priority')

                # date changes
                todo.has_duedate_changed = self.object.tracker.has_changed('duedate')
                todo.has_recur_freq_changed = self.object.tracker.has_changed(
                    'recur_freq')  # returns true if recur_freq field has changed
                todo.has_end_recur_date_changed = self.object.tracker.has_changed(
                    'end_recur_date')  # returns true if end_recur_date has changed

                if (not todo.has_title_changed and not todo.has_duedate_changed and not todo.has_end_recur_date_changed):
                    # find number of future objects ahead of current object being modified
                    future_events = ToDoItem.objects.filter(title__startswith=todo.title,
                                                            duedate__gt=todo.duedate,
                                                            end_recur_date__lte=todo.end_recur_date)
                    todo.count_future_events = len(future_events)
                elif (todo.has_title_changed and not todo.has_duedate_changed and not todo.has_end_recur_date_changed):
                    # find number of future objects ahead of current object being modified
                    future_events = ToDoItem.objects.filter(title__startswith=todo.tracker.previous('title'),
                                                            duedate__gt=todo.duedate,
                                                            end_recur_date__lte=todo.end_recur_date)
                    todo.count_future_events = len(future_events)
                elif (not todo.has_title_changed and todo.has_duedate_changed and not todo.has_end_recur_date_changed):
                    # find number of future objects ahead of current object being modified
                    future_events = ToDoItem.objects.filter(title__startswith=todo.title,
                                                            duedate__gt=todo.tracker.previous('duedate'),
                                                            end_recur_date__lte=todo.end_recur_date)
                    todo.count_future_events = len(future_events)
                elif (not todo.has_title_changed and not todo.has_duedate_changed and todo.has_end_recur_date_changed):
                    # find number of future objects ahead of current object being modified
                    future_events = ToDoItem.objects.filter(title__startswith=todo.title,
                                                            duedate__gt=todo.duedate,
                                                            end_recur_date__lte=todo.tracker.previous('end_recur_date'))
                    todo.count_future_events = len(future_events)
                elif (todo.has_title_changed and todo.has_duedate_changed and not todo.has_end_recur_date_changed):
                    # find number of future objects ahead of current object being modified
                    future_events = ToDoItem.objects.filter(title__startswith=todo.tracker.previous('title'),
                                                            duedate__gt=todo.tracker.previous('duedate'),
                                                            end_recur_date__lte=todo.end_recur_date)
                    todo.count_future_events = len(future_events)
                elif (todo.has_title_changed and not todo.has_duedate_changed and todo.has_end_recur_date_changed):
                    # find number of future objects ahead of current object being modified
                    future_events = ToDoItem.objects.filter(title__startswith=todo.tracker.previous('title'),
                                                            duedate__gt=todo.duedate,
                                                            end_recur_date__lte=todo.tracker.previous('end_recur_date'))
                    todo.count_future_events = len(future_events)
                elif (not todo.has_title_changed and todo.has_duedate_changed and todo.has_end_recur_date_changed):
                    # find number of future objects ahead of current object being modified
                    future_events = ToDoItem.objects.filter(title__startswith=todo.title,
                                                            duedate__gt=todo.tracker.previous('duedate'),
                                                            end_recur_date__lte=todo.tracker.previous('end_recur_date'))
                    todo.count_future_events = len(future_events)
                elif (todo.has_title_changed and todo.has_duedate_changed and todo.has_end_recur_date_changed):
                    # find number of future objects ahead of current object being modified
                    future_events = ToDoItem.objects.filter(title__startswith=todo.tracker.previous('title'),
                                                            duedate__gt=todo.tracker.previous('duedate'),
                                                            end_recur_date__lte=todo.tracker.previous('end_recur_date'))
                    todo.count_future_events = len(future_events)

                todo.save()
                form.save_m2m()

                return redirect('todo_list:change_all', todo_item_id=self.object.id)


def change_all(request, todo_item_id):
    todo_item = get_object_or_404(ToDoItem, pk=todo_item_id)  # get obj
    if (todo_item.has_title_changed):
        for i in range(1, todo_item.count_future_events + 1):
            future_event = ToDoItem.objects.get(pk=todo_item_id + i)
            future_event.title = todo_item.title
            future_event.save()
            todo_item.has_title_changed = False
            todo_item.save()
    if (todo_item.has_description_changed):
        for i in range(1, todo_item.count_future_events + 1):
            future_event = ToDoItem.objects.get(pk=todo_item_id + i)
            future_event.description = todo_item.description
            future_event.save()
            todo_item.has_description_changed = False
            todo_item.save()
    if (todo_item.has_location_changed):
        for i in range(1, todo_item.count_future_events + 1):
            future_event = ToDoItem.objects.get(pk=todo_item_id + i)
            future_event.location = todo_item.location
            future_event.save()
            todo_item.has_location_changed = False
            todo_item.save()
    if (todo_item.has_category_changed):
        for i in range(1, todo_item.count_future_events + 1):
            future_event = ToDoItem.objects.get(pk=todo_item_id + i)
            future_event.category = todo_item.category
            future_event.save()
            todo_item.has_category_changed = False
            todo_item.save()
    if (todo_item.has_priority_changed):
        for i in range(1, todo_item.count_future_events + 1):
            future_event = ToDoItem.objects.get(pk=todo_item_id + i)
            future_event.priority = todo_item.priority
            future_event.save()
            todo_item.has_priority_changed = False
            todo_item.save()
    if (todo_item.has_end_recur_date_changed or todo_item.has_recur_freq_changed or todo_item.has_duedate_changed):
        return redirect('todo_list:edit_recurrences', todo_item_id=todo_item_id)

    return redirect('todo_list:todo_list')


# function checks if user has edited recur_freq field and make according changes to all future tasks
def edit_recurrences(request, todo_item_id):
    todo_item = get_object_or_404(ToDoItem, pk=todo_item_id)  # get obj
    # for date changes, delete all future instances and remake others
    # https://docs.djangoproject.com/en/2.0/ref/models/querysets/
    ToDoItem.objects.filter(title__startswith=todo_item.title,  # filter by title
                            duedate__gt=todo_item.duedate,  # filter by duedate >= todo_item.title
                            end_recur_date__lte=todo_item.end_recur_date
                            ).delete()
    # redirect to create_recurrences to make new future instances
    return redirect('todo_list:create_recurrences', todo_item_id=todo_item_id)


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
    template_name = 'todo/completed_list.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        return ToDoItem.objects.filter(completed=True).order_by('duedate')


def delete_todo(request, todo_item_id):
    item = ToDoItem.objects.get(pk=todo_item_id)
    item.delete()
    return redirect('todo_list:todo_list')


# function changes a to do from incomplete to complete (completed = False -> True)
def completeToDo(request, todo_item_id):
    # To do item to be completed
    completedToDo = ToDoItem.objects.get(id=todo_item_id)
    completedToDo.completed = not completedToDo.completed
    completedToDo.save()

    return redirect('todo_list:todo_list')


################################ Course view ######################################
class AddCourseView(CreateView):
    model = Course
    template_name = "todo/add_course_form.html"
    form_class = CourseForm

    # set title and duedate fields to be required
    def get_form(self, form_class=None):
        form = super(AddCourseView, self).get_form(form_class)
        form.fields['course_name'].required = True
        form.fields['course_abbrev'].required = False
        form.fields['course_prof'].required = False
        return form

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return redirect('todo_list:course_list')


class EditCourseView(UpdateView):
    model = Course
    template_name = "todo/edit_course_form.html"
    form_class = CourseForm

    # set title and duedate fields to be required
    def get_form(self, form_class=None):
        form = super(EditCourseView, self).get_form(form_class)
        form.fields['course_name'].required = True
        form.fields['course_abbrev'].required = False
        form.fields['course_prof'].required = False
        return form

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return redirect('todo_list:course_list')


class CourseListView(generic.ListView):
    template_name = 'todo/course_list.html'
    context_object_name = 'course_list'
    queryset = Course.objects.all().order_by('course_name')


def delete_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    course.delete()
    return redirect('todo_list:course_list')


############################# Academics view ###########################################
class AcademicsListView(generic.ListView):
    template_name = 'todo/academics_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.all().order_by('course_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_course_todo_list'] = ToDoItem.objects.filter(category='AC', course=None)
        return context


############################Extracurricular list view###################################################

class ECListView(generic.ListView):
    template_name = 'todo/ec_list.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
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
        return ToDoItem.objects.filter(completed=False, category='EC').order_by('duedate')


class JobListView(generic.ListView):
    template_name = 'todo/job_list.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
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
        return ToDoItem.objects.filter(completed=False, category='JB').order_by('duedate')


class SocialListView(generic.ListView):
    template_name = 'todo/social_list.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
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
        return ToDoItem.objects.filter(completed=False, category='SC').order_by('duedate')


class PersonalListView(generic.ListView):
    template_name = 'todo/personal_list.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
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
        return ToDoItem.objects.filter(completed=False, category='PS').order_by('duedate')


class OtherListView(generic.ListView):
    template_name = 'todo/other_list.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
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
        return ToDoItem.objects.filter(completed=False, category='OT').order_by('duedate')

# https://stackoverflow.com/questions/15566999/how-to-show-form-input-fields-based-on-select-value
