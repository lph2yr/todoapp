from django.test import TestCase
from .models import ToDoItem
from django.utils import timezone
from django.utils.dateparse import parse_datetime


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
        self.assertIs(day_dif, True)
