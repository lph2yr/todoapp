from django.test import TestCase
from .models import ToDoItem
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.urls import reverse
from .forms import EditToDoForm



def create_todo(new_title, new_description, new_location, new_date_created = timezone.now(), new_duedate = timezone.now(), new_priority = 'LOW', new_completed = False, new_recur_freq = 'NEVER', new_end_recur_date = timezone.now()):
    return ToDoItem.objects.create(
        title = new_title,
        description = new_description,
        location = new_location,
        duedate = new_duedate,
        priority = new_priority,
        completed = new_completed,
        recur_freq = new_recur_freq,
        end_recur_date = new_end_recur_date,
        date_created = new_date_created
    )


class ToDoItemModelTests(TestCase):

    def test_same_is_today_duedate(self):
        """
       returns True if the duedate is the same as currentdate time
        """
        now = timezone.now()
        now = now.replace(tzinfo=None)  # remove timezone info
        # create a new obj
        todo = ToDoItem(
            title="Test case 1",
            description="Testing is_today_duedate",
            location="",
            recur_freq="NEVER",
            duedate=parse_datetime("2020-02-23 09:00")
        )

        day_dif = todo.is_today_duedate()
        self.assertIs(day_dif, False)


#write tests for day view: make sure that only tasks that are due on a certain day are shown


class CreateRecurrences(TestCase):
    def setUp(self):
        create_todo(
            new_title = "Daily test",
            new_recur_freq= 'DAILY',
            new_end_recur_date= make_aware(parse_datetime("2020-03-05 09:00")),
            new_duedate = make_aware(parse_datetime("2020-02-27 08:00")),
            new_description="", #req
            new_location="" #req
        )

        #blank
        create_todo(
            new_title = "",
            new_recur_freq='NEVER',
            new_end_recur_date=make_aware(parse_datetime("2020-03-05 09:00")),
            new_duedate=make_aware(parse_datetime("2020-02-27 08:00")),
            new_description="Blank title",  # req
            new_location=""  # req
        )
    def is_correct_template_used(self):
        todo = ToDoItem.objects.get(title="Daily test")
        pk = todo.id
        response = self.client.get(reverse('todo_list:detail', args=[pk]))
        self.assertEqual(response.status_code, 200)

        #check correct template used
        self.assertTemplateUsed(response, 'todo/edit_todoitem_form.html')

    #test display req message