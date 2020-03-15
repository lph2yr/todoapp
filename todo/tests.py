from django.test import TestCase, Client
from .models import ToDoItem
from django.utils import timezone
from django.urls import reverse
import pytz
import datetime

def create_todo(new_title,
                new_description,
                new_location,
                new_duedate=timezone.now(),
                new_priority='LO',
                new_completed=False,
                new_recur_freq='NEVER',
                new_end_recur_date=timezone.now(),
                new_category='NN',
                new_course=None
                ):
    return ToDoItem.objects.create(
        title=new_title,
        description=new_description,
        location=new_location,
        duedate=new_duedate,
        priority=new_priority,
        completed=new_completed,
        recur_freq=new_recur_freq,
        end_recur_date=new_end_recur_date,
        category = new_category,
        course = new_course,
    )


class ToDoItemModelTests(TestCase):
    def test_same_is_today_duedate(self):
        """
       returns True if the duedate is the same as currentdate time
        """
        # create a new obj
        #naive = parse_datetime("2020-03-15 10:28:45")
        #pytz.timezone("America/New_York").localize(naive, is_dst=None)
        todo = ToDoItem(
            title="Test case 1",
            description="Testing is_today_duedate",
            location="",
            recur_freq="NEVER",
            duedate=datetime.datetime(2020, 3, 15, 6, 0, 0, tzinfo=pytz.utc)
        )

        day_dif = todo.is_today_duedate()
        self.assertIs(day_dif, True)


# write tests for day view: make sure that only tasks that are due on a certain day are shown


class CreateRecurrences(TestCase):
    def setUp(self):

        create_todo(
            new_title="Daily test",
            new_description="",  # req
            new_location="",  # req
            new_duedate=datetime.datetime(2020, 3, 15, 6, 0, 0, tzinfo=pytz.utc),
            new_recur_freq='DAILY',
            new_end_recur_date=datetime.datetime(2020, 3, 31, 5, 0, 0, tzinfo=pytz.utc),
        )

        create_todo(
            new_title="Weekly test",
            new_description="",  # req
            new_location="",  # req
            new_duedate=datetime.datetime(2020, 2, 27, 6, 0, 0, tzinfo=pytz.utc),
            new_recur_freq='WEEKLY',
            new_end_recur_date=datetime.datetime(2020, 4, 20, 9, 0, 0, tzinfo=pytz.utc)
        )

        create_todo(
            new_title="Monthly test",
            new_description="",  # req
            new_location="",  # req
            new_duedate=datetime.datetime(2020, 2, 27, 6, 0, 0, tzinfo=pytz.utc),
            new_recur_freq='MONTHLY',
            new_end_recur_date=datetime.datetime(2020, 6, 20, 6, 0, 0, tzinfo=pytz.utc),
        )

        create_todo(
            new_title="Yearly test",
            new_description="",  # req
            new_location="",  # req
            new_duedate=datetime.datetime(2020, 2, 27, 6, 0, 0, tzinfo=pytz.utc),
            new_recur_freq='YEARLY',
            new_end_recur_date=datetime.datetime(2025, 6, 20, 6, 0, 0, tzinfo=pytz.utc),
        )

    def test_is_correct_template_used(self):
        """
        Test that the correct template is used when user wants to create recurrences
        """
        todo = ToDoItem.objects.get(title="Daily test")
        pk = todo.id
        response = self.client.get(reverse('todo_list:detail', args=[pk]))
        self.assertEqual(response.status_code, 200)

        # check correct template used
        self.assertTemplateUsed(response, 'todo/edit_todoitem_form.html')

    # test display req message
    def daily_recurrences_are_made(self):
        """
        Tests whether daily recurrences are made
        """
        response = self.client.get(reverse('todo_list:todo_list'))
        compare_list = ToDoItem.objects.filter(title = 'Daily test',
                                               duedate__gte = datetime.datetime(2020, 3, 15, 6, 0, 0, tzinfo=pytz.utc),
                                               end_recur_date = datetime.datetime(2020, 3, 31, 5, 0, 0, tzinfo=pytz.utc))
        self.assertQuerysetEqual(
            response.context['todo_list'],
            compare_list
        )

    def weekly_recurrences_are_made(self):
        """
        Tests whether weekly recurrences are made
        """
        response = self.client.get(reverse('todo_list:todo_list'))
        compare_list = ToDoItem.objects.filter(title = 'Weekly test',
                                               duedate__gte = datetime.datetime(2020, 2, 27, 6, 0, 0, tzinfo=pytz.utc),
                                               end_recur_date = datetime.datetime(2020, 4, 20, 9, 0, 0, tzinfo=pytz.utc))
        self.assertQuerysetEqual(
            response.context['todo_list'],
            compare_list
        )

    def monthly_recurrences_are_made(self):
        """
        Tests whether monthly recurrences are made
        """
        response = self.client.get(reverse('todo_list:todo_list'))
        compare_list = ToDoItem.objects.filter(title = 'Monthly test',
                                               duedate__gte = datetime.datetime(2020, 2, 27, 6, 0, 0, tzinfo=pytz.utc),
                                               end_recur_date =datetime.datetime(2020, 6, 20, 6, 0, 0, tzinfo=pytz.utc))
        self.assertQuerysetEqual(
            response.context['todo_list'],
            compare_list
        )

    def yearly_recurrences_are_made(self):
        """
        Tests whether yearly recurrences are made
        """
        response = self.client.get(reverse('todo_list:todo_list'))
        compare_list = ToDoItem.objects.filter(title = 'Yearly test',
                                               duedate__gte = datetime.datetime(2020, 2, 27, 6, 0, 0, tzinfo=pytz.utc),
                                               end_recur_date = datetime.datetime(2025, 6, 20, 6, 0, 0, tzinfo=pytz.utc))
        self.assertQuerysetEqual(
            response.context['todo_list'],
            compare_list
        )

class PriorityTest(TestCase):
    def setUp(self):
        create_todo(
            new_title="priority test",
            new_priority="HI",
            new_duedate=datetime.datetime(2020, 2, 27, 8, 0, 0, tzinfo=pytz.utc),
            new_description="",
            new_location=""
        )

    def test_check_priority(self):
        response = self.client.get(reverse('todo_list:todo_list'))
        l = response.context['todo_list']
        todo = l[0] #only item in list
        self.assertEqual(todo.title, "priority test")
        self.assertEqual(todo.priority, "HI")


class TodoListViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo_list:todo_list'))
        self.assertEqual(response.status_code, 200)
        # this view doesn't have a context object...it only has context_data