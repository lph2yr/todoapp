from django.test import TestCase, Client
from .models import ToDoItem
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.urls import reverse
from .forms import ToDoForm


def create_todo(new_title,
                new_description,
                new_location,
                new_duedate=timezone.now(),
                new_priority='LO',
                new_completed=False,
                new_recur_freq='NEVER',
                new_end_recur_date=timezone.now(),
                new_category='NN',
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
        category = new_category
    )


class ToDoItemModelTests(TestCase):
    def test_same_is_today_duedate(self):
        """
       returns True if the duedate is the same as currentdate time
        """
        # create a new obj
        todo = ToDoItem(
            title="Test case 1",
            description="Testing is_today_duedate",
            location="",
            recur_freq="NEVER",
            duedate=make_aware(parse_datetime("2020-02-23 09:00"))
        )

        day_dif = todo.is_today_duedate()
        self.assertIs(day_dif, False)


# write tests for day view: make sure that only tasks that are due on a certain day are shown


class CreateRecurrences(TestCase):
    def setUp(self):
        create_todo(
            new_title="Daily test",
            new_description="",  # req
            new_location="",  # req
            new_duedate=make_aware(parse_datetime("2020-02-27 08:00")),
            new_recur_freq='DAILY',
            new_end_recur_date=make_aware(parse_datetime("2020-03-02 09:00")),
        )

        create_todo(
            new_title="Weekly test",
            new_description="",  # req
            new_location="",  # req
            new_duedate=make_aware(parse_datetime("2020-02-27 08:00")),
            new_recur_freq='WEEKLY',
            new_end_recur_date=make_aware(parse_datetime("2020-04-20 09:00")),
        )

        create_todo(
            new_title="Monthly test",
            new_description="",  # req
            new_location="",  # req
            new_duedate=make_aware(parse_datetime("2020-02-27 08:00")),
            new_recur_freq='MONTHLY',
            new_end_recur_date=make_aware(parse_datetime("2020-06-20 09:00")),
        )

        create_todo(
            new_title="Yearly test",
            new_description="",  # req
            new_location="",  # req
            new_duedate=make_aware(parse_datetime("2020-02-27 08:00")),
            new_recur_freq='MONTHLY',
            new_end_recur_date=make_aware(parse_datetime("2025-06-20 09:00")),
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
                                               duedate__gte = make_aware(parse_datetime("2020-02-27 08:00")),
                                               end_recur_date = make_aware(parse_datetime("2020-03-02 09:00")))
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
                                               duedate__gte = make_aware(parse_datetime("2020-02-27 08:00")),
                                               end_recur_date = make_aware(parse_datetime("2020-04-20 09:00")))
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
                                               duedate__gte = make_aware(parse_datetime("2020-02-27 08:00")),
                                               end_recur_date = make_aware(parse_datetime("2020-06-20 09:00")))
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
                                               duedate__gte = make_aware(parse_datetime("2020-02-27 08:00")),
                                               end_recur_date = make_aware(parse_datetime("2025-06-20 09:00")))
        self.assertQuerysetEqual(
            response.context['todo_list'],
            compare_list
        )

class PriorityTest(TestCase):
    def setUp(self):
        create_todo(
            new_title="priority test",
            new_priority="HI",
            new_duedate=make_aware(parse_datetime("2020-02-27 08:00")),
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