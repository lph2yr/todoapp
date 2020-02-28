from django.test import TestCase
from .models import ToDoItem
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.urls import reverse
from django.utils.timezone import make_aware
import datetime

# Create your tests here.

def create_todo(new_title, new_description, new_location, new_duedate = timezone.now(), new_priority = 'LOW', new_completed = False, new_recur_freq = 'NEVER', new_end_recur_date = timezone.now()):
    return ToDoItem.objects.create(
        title = new_title,
        description = new_description,
        location = new_location,
        duedate = new_duedate,
        priority = new_priority,
        completed = new_completed,
        recur_freq = new_recur_freq,
        end_recur_date = new_end_recur_date
    )


class ToDoItemModelTests(TestCase):

    def test_same_is_today_duedate(self):
        """
       returns True if the duedate is the same as currentdate time
        """
        now = timezone.now()
        now = now.replace(tzinfo=None)  # remove timezone info
        #create a new obj
        todo = ToDoItem(
            title = "Test case 1",
            description = "Testing is_today_duedate",
            location = "",
            recur_freq = "NEVER",
            duedate = parse_datetime("2020-02-23 09:00")
        )

        day_dif = todo.is_today_duedate()
        self.assertIs(day_dif, False)

class AddToDoTests(TestCase):

    """
    def test_todo_created(self):
        ToDoItem.objects.create(title= "Test add",
                        description="Test added",
                        duedate= timezone.now(),
                        recur_freq = 'NEVER',
                        end_recur_date = timezone.now() + datetime.timedelta(days=5)
                                )
    """


class ToDoEditTests(TestCase):

    def test_edit_title(self):
        """
        returns True if title is edited/different
        """
        todo = create_todo("Test title", "This is the test for editing title", "Apartment")
        url = reverse('todo_list:detail', kwargs={'pk': todo.id})
        new_title = {'title': todo.title, 'duedate': todo.duedate, 'recur_freq': todo.recur_freq, 'end_recur_date': todo.end_recur_date}
        response = self.client.post(url, new_title)
        self.assertEqual(response.status_code, 302)
        todo.refresh_from_db()
        self.assertEqual(todo.title, "Test title edited" )
