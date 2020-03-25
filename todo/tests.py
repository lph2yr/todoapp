from django.test import TestCase, Client
from .models import ToDoItem, Course, Extracurricular
from .forms import ToDoForm
from django.utils import timezone
from django.urls import reverse
import datetime
from dateutil.relativedelta import relativedelta
import pytz

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

#if there is a dictionary of fields already available, use this function with the dictionary as parameter
def create_from_data_dict( form_data ):
    form = ToDoForm(data = form_data)
    return form.save()


def create_course(
        new_course_name,
        new_course_abbrev = "",
        new_course_prof = "",
):
    return Course.objects.create(
        course_name = new_course_name,
        course_abbrev = new_course_abbrev,
        course_prof = new_course_prof
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
        self.course = create_course(new_course_name="Tester")
        self.ec = create_ec(new_name='')

    def test_same_is_today_duedate(self):
        """
       returns True if the duedate is the same as currentdate time
        """
        # create a new obj
        todo = ToDoItem(
            title="Test case 1",
            duedate=datetime.datetime(2020, 2, 23, 9, 0),
            course=self.course,
            ec=self.ec
        )

        day_dif = todo.is_today_duedate()
        self.assertIs(day_dif, False)


class PriorityTest(TestCase):
    def setUp(self):
        self.my_course = create_course(
            new_course_name="Tester"
        )
        self.my_ec = create_ec(new_name='fun')
        create_todo(
            new_title="priority test",
            new_priority="HI",
            new_duedate=datetime.datetime(2020, 2, 27, 8, 0, 0, tzinfo=pytz.utc),
            new_course=self.my_course,
            new_ec=self.my_ec
        )

    def test_check_priority(self):
        response = self.client.get(reverse('todo_list:todo_list'))
        l = response.context['todo_list']
        todo = l[0]  # only item in list
        self.assertEqual(todo.title, "priority test")
        self.assertEqual(todo.priority, "HI")


class DayViewTest(TestCase):
    def setUp(self):
        self.course = create_course(new_course_name="Tester")
        self.ec = create_ec(new_name='')

        create_todo(
            new_title="March 5th todo",
            new_duedate=datetime.datetime(2020, 3, 5, 9, 0),
            new_completed=False,
            new_course=self.course,
            new_ec=self.ec,
        )

        self.complete_3_5 = create_todo(
            new_title="March 5th todo completed",
            new_duedate=datetime.datetime(2020, 3, 5, 9, 0),
            new_course=self.course,
            new_ec=self.ec,
        )
        self.complete_3_5.completed = True
        self.complete_3_5.save()

        mar17_todo = create_todo(
            new_title="March 17th todo",
            new_duedate=datetime.datetime(2020, 3, 17, 14, 0),
            new_course=self.course,
            new_ec=self.ec,
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

class ToDoItemFormTest(TestCase):
    """
    Test whether CreateView is successful
    """
    def setUp(self):
        self.my_course = create_course(
            new_course_name="Tester"
        )

        self.my_ec = create_ec(new_name='fun')

        #this data will be passed into the Forms and create/update object
        self.data_form = {
            'title': "TBD",
            'description': '',
            'duedate': timezone.now(),
            'location': '',
            'recur_freq': 'NEVER',
            'end_recur_date': timezone.now(),
            'priority': 'LO',
            'category': 'NN',
            'course': self.my_course,
            'ec': self.my_ec,
            'progress':0
            }

    def test_todoitemform_success_submission(self):
        self.data_form['title'] = 'Test submission success'
        form = ToDoForm(data=self.data_form)
        self.assertTrue(form.is_valid())

    def test_correct_template_for_add_todo(self):
        self.data_form['title'] = "Test correct template used"
        response = self.client.post( reverse('todo_list:add_todo_item'),self.data_form )
        self.assertEqual(response.status_code, 200)

        #make sure that add todo form is used
        self.assertTemplateUsed(response, 'todo/todoitem_form.html')

    def tearDown(self):
        del self.my_course
        del self.data_form

class CreateDailyRecurrencesTest(TestCase):
    def setUp(self):
        self.my_course = create_course(
            new_course_name="Tester"
        )
        self.my_ec = create_ec(new_name='fun')

        self.data_form = {
            'title': "TBD",
            'description': '',
            'duedate': datetime.datetime(2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc),
            'location': '',
            'recur_freq': 'DAILY',
            'end_recur_date': datetime.datetime(2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc),
            'priority': 'LO',
            'category': 'NN',
            'course': self.my_course.id,
            'ec': self.my_ec.id,
            'progress':0
        }

    def test_create_daily_recurrences_equiv(self):# equivalence test
        """
        Tests whether create_recurrenes work
        """
        self.data_form['title'] = "Test creating daily recurrences"
        self.data_form['description'] = "Some end_recur_date at the same time"
        self.data_form['end_recur_date'] = datetime.datetime(2020, 3, 19, 5, 0, 0, tzinfo=pytz.utc)

        daily_occurrence = create_from_data_dict(self.data_form) #create first instance

        #should create 4 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': daily_occurrence.id}), self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual( 4, len(current_query_set))

        #check crucial fields
        filtered = ToDoItem.objects.filter(title='Test creating daily recurrences',
                                           description = "Some end_recur_date at the same time",
                                            recur_freq='DAILY',
                                              end_recur_date=datetime.datetime(2020, 3, 19, 5, 0, 0, tzinfo=pytz.utc))
        self.assertEqual(4, len(filtered))

        count_true = 0
        #check due date
        for i in range( len(filtered) - 1):
            if filtered[i].duedate == filtered[i+1].duedate - datetime.timedelta(days=1):
                count_true += 1

        #count_true has to be 3 because 3 comparisons if test works
        self.assertEqual(3, count_true )

    def test_redirect_from_create_recurrences_to_todo_list(self):
        """
        Test that after a successful create_recurrences, it redirects to todo_list
        """
        self.data_form['title'] = "Test redirect to list after creating_recurrences"
        self.data_form['recur_freq'] = 'DAILY'
        self.data_form['end_recur_date'] = datetime.datetime(2020, 3, 31, 5, 0, 0, tzinfo=pytz.utc)
        daily_occurrence = create_from_data_dict(self.data_form)

        response = self.client.post(
            reverse('todo_list:create_recurrences', kwargs={'todo_item_id': daily_occurrence.id}), self.data_form)
        self.assertRedirects(response, reverse('todo_list:todo_list'))

    def test_create_daily_recurrences_shorter_time(self):# boundary test
        """
        Some end_recur_date not a full day from duedate
        """
        self.data_form['title'] = "Test creating daily recurrences"
        self.data_form['description'] = "Some end_recur_date but with an earlier time than duedate"
        self.data_form['end_recur_date'] = datetime.datetime(2020, 3, 19, 4, 0, 0, tzinfo=pytz.utc)

        daily_occurrence = create_from_data_dict(self.data_form) #create first instance

        #should create 3 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': daily_occurrence.id}), self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual( 3, len(current_query_set))

        #check crucial fields
        filtered = ToDoItem.objects.filter(title='Test creating daily recurrences',
                                         description="Some end_recur_date but with an earlier time than duedate",
                                         recur_freq='DAILY',
                                         end_recur_date=datetime.datetime(2020, 3, 19, 4, 0, 0, tzinfo=pytz.utc)).order_by('duedate')
        self.assertEqual( 3, len(filtered))

        #check duedates of all 3 objects
        count_true = 0
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - datetime.timedelta(days=1):
                count_true += 1

        # count_true has to be 2 because 2 comparisons if test works
        self.assertEqual(2, count_true)


    def test_end_date_earlier_than_duedate(self):
        """
        Create end_recur_date earlier than duedate --> should create only one instance
        """
        self.data_form['title'] = "Test creating daily recurrences"
        self.data_form['description'] = "Some end_recur_date earlier than duedate"
        self.data_form['end_recur_date'] = datetime.datetime(2020, 3, 14, 4, 0, 0, tzinfo=pytz.utc)

        daily_occurrence = create_from_data_dict(self.data_form) #create first instance
        #should create 1 instance
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': daily_occurrence.id}), self.data_form)
        current_instance = ToDoItem.objects.get(description="Some end_recur_date earlier than duedate")
        all_instances = [current_instance]

        self.assertEqual( 1, len(all_instances))

        #check crucial fields
        one_instance = ToDoItem.objects.get(title ="Test creating daily recurrences",
                                         description="Some end_recur_date earlier than duedate",
                                         end_recur_date=datetime.datetime(2020, 3, 14, 4, 0, 0, tzinfo=pytz.utc))

        #check duedates of all 1 object
        self.assertEqual( one_instance.duedate, datetime.datetime(2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc))

    def tearDown(self):
        del self.data_form
        del self.my_course
        del self.my_ec


class CreateWeeklyRecurrencesTests(TestCase):
    def setUp(self):
        self.my_course = create_course(
            new_course_name="Tester"
        )

        self.my_ec = create_ec(new_name='fun')

        # this data will be passed into the Forms and create/update object
        self.data_form = {
            'title': "Test creating weekly recurrences equivalence",
            'description': '',
            'duedate': datetime.datetime(2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc),
            'location': '',
            'recur_freq': 'WEEKLY',
            'end_recur_date': datetime.datetime(2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc),
            'priority': 'LO',
            'category': 'NN',
            'course': self.my_course,
            'ec': self.my_ec,
            'progress': 0
        }

    def test_create_weekly_recurrences_equiv(self):  # equivalence test
        """
        Equivalence Tests for creating weekly recurrences
        """
        self.data_form['end_recur_date'] = datetime.datetime(2020, 4, 6, 5, 0, 0,
                                                             tzinfo=pytz.utc)

        weekly_occurrence = create_from_data_dict(self.data_form)  # create first instance

        # should create 4 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': weekly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(4, len(current_query_set))

        # check crucial fields
        filtered = ToDoItem.objects.filter(title="Test creating weekly recurrences equivalence",
                                           recur_freq='WEEKLY',
                                           end_recur_date=datetime.datetime(2020, 4, 6, 5, 0, 0,
                                                                            tzinfo=pytz.utc)).order_by('duedate')
        self.assertEqual(4, len(filtered))

        # check duedates of all 4 objects
        count_true = 0
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(weeks=1):
                count_true += 1

        # count_true has to be 3 because 3 comparisons if test works
        self.assertEqual(3, count_true)
'''
    ################## boundary tests ######################
    def test_create_less_than_a_full_week(self):
        """
        end_recur_date is not a full 4 weeks --> should create only 3 instances
        """
        self.data_form['title'] = "Test creating weekly recurrences boundaries"
        self.data_form['description'] = "end_recur_date is not a full 4 weeks"
        self.data_form['end_recur_date'] = datetime.datetime(2020, 4, 5, 5, 0, 0, tzinfo=pytz.utc)

        weekly_occurrence = create_from_data_dict(self.data_form)  # create first instance

        # should create 3 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': weekly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(3, len(current_query_set))

        # check crucial fields
        filtered = ToDoItem.objects.filter(title="Test creating weekly recurrences boundaries",
                                           description="end_recur_date is not a full 4 weeks",
                                           recur_freq='WEEKLY',
                                           end_recur_date=datetime.datetime(2020, 4, 5, 5, 0, 0, tzinfo=pytz.utc)
                                           ).order_by('duedate')
        self.assertEqual(3, len(filtered))

        # check duedates of all 3 objects
        count_true = 0
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(weeks=1):
                count_true += 1

        # count_true has to be 2 because 2 comparisons if test works
        self.assertEqual(2, count_true)

    def test_create_more_than_a_full_week(self):
        """
        end_recur_date is more than a full 4 weeks --> should create 4 instances
        """
        self.data_form['title'] = "Test creating weekly recurrences boundaries"
        self.data_form['description'] = "end_recur_date is more than 4 weeks but less than 5 weeks"
        self.data_form['end_recur_date'] = datetime.datetime(2020, 4, 8, 5, 0, 0, tzinfo=pytz.utc)

        weekly_occurrence = create_from_data_dict(self.data_form)  # create first instance

        # should create 3 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': weekly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(4, len(current_query_set))

        # check crucial fields
        # check titles
        filtered = ToDoItem.objects.filter(title="Test creating weekly recurrences boundaries",
                                           description="end_recur_date is more than 4 weeks but less than 5 weeks",
                                           recur_freq='WEEKLY',
                                           end_recur_date=datetime.datetime(2020, 4, 8, 5, 0, 0, tzinfo=pytz.utc)
                                           ).order_by('duedate')
        self.assertEqual(4, len(filtered))

        # check duedates of all 4 objects
        count_true = 0
        # check due date
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(weeks=1):
                count_true += 1

        # count_true has to be 3 because 3 comparisons if test works
        self.assertEqual(3, count_true)

    def test_create_full_week_but_less_time(self):
        """
        end_recur_date is not a full 4 weeks --> should create only 3 instances
        """
        self.data_form['title'] = "Test creating weekly recurrences boundaries"
        self.data_form['description'] = "end_recur_date is 4 weeks by day but not 4 weeks by time"
        self.data_form['end_recur_date'] = datetime.datetime(2020, 4, 5, 3, 0, 0, tzinfo=pytz.utc)

        weekly_occurrence = create_from_data_dict(self.data_form)  # create first instance

        # should create 3 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': weekly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(3, len(current_query_set))

        # check crucial fields
        filtered = ToDoItem.objects.filter(title="Test creating weekly recurrences boundaries",
                                           description="end_recur_date is 4 weeks by day but not 4 weeks by time",
                                           recur_freq='WEEKLY',
                                           end_recur_date=datetime.datetime(2020, 4, 5, 3, 0, 0, tzinfo=pytz.utc)
                                           ).order_by('duedate')
        self.assertEqual(3, len(filtered))

        # check duedates of all 3 objects
        count_true = 0
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(weeks=1):
                count_true += 1
        # count_true has to be 2 because 2 comparisons if test works
        self.assertEqual(2, count_true)

    def test_end_date_earlier_than_duedate_weekly(self):
        """
        Create end_recur_date earlier than duedate --> should create only one instance
        """
        self.data_form['title'] = "Test creating weekly recurrences"
        self.data_form['description'] = "Some end_recur_date earlier than duedate"
        self.data_form['end_recur_date'] = datetime.datetime(2020, 3, 10, 4, 0, 0, tzinfo=pytz.utc)

        weekly_occurrence = create_from_data_dict(self.data_form)  # create first instance
        # print( daily_occurrence.id )
        # should create 1 instance
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': weekly_occurrence.id}),
                         self.data_form)
        current_instance = ToDoItem.objects.get(description="Some end_recur_date earlier than duedate")
        all_instances = [current_instance]

        self.assertEqual(1, len(all_instances))

        # check crucial fields
        one_instance = ToDoItem.objects.get(title="Test creating weekly recurrences",
                                            description="Some end_recur_date earlier than duedate",
                                            end_recur_date=datetime.datetime(2020, 3, 10, 4, 0, 0, tzinfo=pytz.utc))

        # check duedates of  1 object
        self.assertEqual(one_instance.duedate, datetime.datetime(2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc))

    def tearDown(self):
        del self.data_form
        del self.my_course
        del self.my_ec

'''
