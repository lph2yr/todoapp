from django.test import TestCase, Client
from .models import ToDoItem
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.urls import reverse
from .forms import ToDoForm
from .views import DayView, SpecificDayView

def create_todo(new_title, new_description, new_location, new_date_created=timezone.now(),
                new_duedate=timezone.now(), new_priority='LO', new_completed=False,
                new_recur_freq='NEVER', new_end_recur_date=timezone.now()):
    return ToDoItem.objects.create(
        title=new_title,
        description=new_description,
        location=new_location,
        duedate=new_duedate,
        priority=new_priority,
        completed=new_completed,
        recur_freq=new_recur_freq,
        end_recur_date=new_end_recur_date,
        # date_created=new_date_created
    )


class ToDoItemModelTests(TestCase):
    def test_same_is_today_duedate(self):
        """
       returns True if the duedate is the same as currentdate time
        """
        now = timezone.now()
        # create a new obj
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


class CreateRecurrences(TestCase):
    def setUp(self):
        create_todo(
            new_title="Daily test",
            new_recur_freq='DAILY',
            new_end_recur_date=make_aware(parse_datetime("2020-03-05 09:00")),
            new_duedate=make_aware(parse_datetime("2020-02-27 08:00")),
            new_description="",  # req
            new_location=""  # req
        )

        # blank
        create_todo(
            new_title="",
            new_recur_freq='NEVER',
            new_end_recur_date=make_aware(parse_datetime("2020-03-05 09:00")),
            new_duedate=make_aware(parse_datetime("2020-02-27 08:00")),
            new_description="Blank title",  # req
            new_location=""  # req
        )

    def test_is_correct_template_used(self):
        todo = ToDoItem.objects.get(title="Daily test")
        pk = todo.id
        response = self.client.get(reverse('todo_list:detail', args=[pk]))
        self.assertEqual(response.status_code, 200)

        # check correct template used
        self.assertTemplateUsed(response, 'todo/edit_todoitem_form.html')

    # test display req message


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
        todo = ToDoItem.objects.get(title="priority test")
        self.assertEqual(todo.priority, "HI")


class DayViewTest(TestCase):

    def setUp(self):
        create_todo(
            new_title="March 5th todo", 
            new_description="", 
            new_location="", 
            new_date_created=timezone.now(),
            new_duedate=make_aware(parse_datetime("2020-03-05 14:00")), 
            new_priority='LO', 
            new_completed=False,
            new_recur_freq='NEVER', 
            new_end_recur_date=timezone.now())
        
        create_todo(
            new_title="March 5th todo completed", 
            new_description="", 
            new_location="", 
            new_date_created=timezone.now(),
            new_duedate=make_aware(parse_datetime("2020-03-05 14:00")), 
            new_priority='LO', 
            new_completed=True,
            new_recur_freq='NEVER', 
            new_end_recur_date=timezone.now())

        mar17_todo = create_todo(
            new_title="March 17th todo", 
            new_description="", 
            new_location="", 
            new_date_created=timezone.now(),
            new_duedate=make_aware(parse_datetime("2020-03-17 14:00")), 
            new_priority='LO', 
            new_completed=False,
            new_recur_freq='NEVER', 
            new_end_recur_date=timezone.now())

    def test_check_no_todos(self):
        response = self.client.get('/day/2020/mar/12/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have no to-do items for this day!")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_check_one_todo(self):
        response = self.client.get('/day/2020/mar/17/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "March 17th todo")
        self.assertQuerysetEqual(response.context['object_list'], ['<ToDoItem: March 17th todo 2020-03-17>'])

    def test_check_only_incomplete_todo(self):
        response = self.client.get('/day/2020/mar/5/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "March 5th todo")
        self.assertNotContains(response, "March 5th todo completed")
        self.assertQuerysetEqual(response.context['object_list'], ['<ToDoItem: March 5th todo 2020-03-05>'])

        
class TodoListViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo_list:todo_list'))
        self.assertEqual(response.status_code, 200)
        # this view doesn't have a context object...it only has context_data
