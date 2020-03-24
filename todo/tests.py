from django.test import TestCase, Client
from .models import ToDoItem, Course, Extracurricular
from django.utils import timezone
from django.urls import reverse
import datetime

def create_todo(new_title, #only need to provide title if everything else is unchanged
                new_description='',
                new_location='',
                new_duedate=timezone.now(),
                new_priority='LO',
                new_completed=False,
                new_recur_freq='NEVER',
                new_end_recur_date=timezone.now(),
                new_course=None,
                new_ec = None,
                new_progress = 0,
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
        course = new_course,
        ec = new_ec,
        progress = new_progress
    )

def create_course(
        new_name,
        new_abbrev = "",
        new_prof = "",
):
    return Course.objects.create(
        course_name = new_name,
        course_abbrev = new_abbrev,
        course_prof = new_prof
    )

def create_ec(
        new_name,
        new_details = '',
        new_start_date = datetime.date.today(),
        new_end_date = datetime.date.today(),
        new_active = True,
):
    return Extracurricular.objects.create(
        name = new_name,
        detail = new_details,
        start_date = new_start_date,
        end_date = new_end_date,
        active = new_active
    )

class ToDoItemModelTests(TestCase):
    def setUp(self):
        self.course = create_course(new_name="Tester")
        self.ec = create_ec(new_name='')

    def test_same_is_today_duedate(self):
        """
       returns True if the duedate is the same as currentdate time
        """
        # create a new obj
        todo = ToDoItem(
            title="Test case 1",
            duedate=datetime.datetime(2020, 2, 23, 9, 0),
            course = self.course,
            ec = self.ec
        )

        day_dif = todo.is_today_duedate()
        self.assertIs(day_dif, False)


class CreateRecurrences(TestCase):
    def setUp(self):
        course = create_course(new_name="Tester")
        ec = create_ec(new_name='')
        create_todo(
            new_title="Daily test",
            new_duedate=datetime.datetime(2020, 2, 27, 9, 0),
            new_recur_freq='DAILY',
            new_end_recur_date=datetime.datetime(2020, 3, 5, 9, 0),
            new_course = course,
            new_ec = ec,
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
        self.course = create_course(new_name="Tester")
        self.ec = create_ec(new_name='')
        create_todo(
            new_title="priority test",
            new_priority="HI",
            new_duedate=datetime.datetime(2020, 2, 27, 8, 0),
            new_course = self.course,
            new_ec = self.ec,
        )

    def test_check_priority(self):
        todo = ToDoItem.objects.get(title="priority test")
        self.assertEqual(todo.priority, "HI")


class DayViewTest(TestCase):
    def setUp(self):
        course = create_course(new_name="Tester")
        ec = create_ec(new_name='')
        create_todo(
            new_title="March 5th todo",
            new_duedate=datetime.datetime(2020, 3, 5, 9, 0),
            new_course = course,
            new_ec = ec,
        )
        
        create_todo(
            new_title="March 5th todo completed",
            new_duedate=datetime.datetime(2020, 3, 5, 9, 0),
            new_completed=True,
            new_course = course,
            new_ec = ec,
        )

        mar17_todo = create_todo(
            new_title="March 17th todo",
            new_duedate=datetime.datetime(2020, 3, 17, 14, 0),
            new_course = course,
            new_ec = ec,
        )

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
