from django.test import TestCase, Client
from .models import ToDoItem, Course, Extracurricular, Note
from .forms import ToDoForm
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
from dateutil.relativedelta import relativedelta
import pytz


def create_todo(new_title,  # only need to provide title if everything else is unchanged
                new_description='',
                new_location='',
                new_duedate=timezone.now(),
                new_priority='LO',
                new_completed=False,
                new_recur_freq='NEVER',
                new_end_recur_date=timezone.now(),
                new_category='NN',
                new_course=None,
                new_ec=None,
                new_progress=0,
                user='',
                ):
    form_data = {'title': new_title,
                 'description': new_description,
                 'location': new_location,
                 'duedate': new_duedate,
                 'priority': new_priority,
                 'completed': new_completed,
                 'recur_freq': new_recur_freq,
                 'end_recur_date': new_end_recur_date,
                 'category': new_category,
                 'course': new_course,
                 'ec': new_ec,
                 'progress': new_progress,
                 }
    form = ToDoForm(data=form_data)
    return form.save()

# if there is a dictionary of fields already available, use this function with the dictionary as parameter


def create_from_data_dict(form_data):
    form = ToDoForm(data=form_data)
    return form.save()


def create_course(
        new_course_name,
        new_course_abbrev="",
        new_course_prof="",
        user=None
):
    return Course.objects.create(
        course_name=new_course_name,
        course_abbrev=new_course_abbrev,
        course_prof=new_course_prof,
        user=user
    )


def create_ec(
        new_name,
        new_details='',
        new_start_date=datetime.date.today(),
        new_end_date=datetime.date.today(),
        new_active=True,
        user=None
):
    return Extracurricular.objects.create(
        name=new_name,
        detail=new_details,
        start_date=new_start_date,
        end_date=new_end_date,
        active=new_active,
        user=user)


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
            ec=self.ec,
        )

        day_dif = todo.is_today_duedate()
        self.assertIs(day_dif, False)


class PriorityTest(TestCase):
    def setUp(self):
        # Forces a login to occur, creates a test user if one does not exist
        self.client.force_login(
            User.objects.get_or_create(username='testuser')[0])

        self.my_course = create_course(
            new_course_name="Tester"
        )
        self.my_ec = create_ec(new_name='fun')

        create_todo(
            new_title="priority test",
            new_priority="HI",
            new_duedate=datetime.datetime(
                2020, 2, 27, 8, 0, 0, tzinfo=pytz.utc),
            new_course=self.my_course.id,
            new_ec=self.my_ec.id,
        )

    def test_check_priority(self):
        response = self.client.get(reverse('todo_list:todo_list'))
        l = ToDoItem.objects.all()
        todo = l[0]  # only item in list
        self.assertEqual(todo.title, "priority test")
        self.assertEqual(todo.priority, "HI")


"""
class SpecificDayViewTest(TestCase):
    def setUp(self):
        testuser = User.objects.create_user(username='testuser', password='testpass')
        testuser.save()

        self.client.login(username='testuser', password='testpass')

        self.user = testuser

        self.course = create_course(new_course_name="Tester")
        #self.course.user = testuser
        self.ec = create_ec(new_name='ec')
        #self.ec.user=testuser

        create_todo(
            new_title="March 5th todo",
            new_duedate=datetime.datetime(2020, 3, 5, 9, 0),
            new_completed=False,
            new_course=self.course.id,
            new_ec=self.ec.id,
            user=testuser,
        )

        self.complete_3_5 = create_todo(
            new_title="March 5th todo completed",
            new_duedate=datetime.datetime(2020, 3, 5, 9, 0),
            new_course=self.course.id,
            new_ec=self.ec.id,
            user=testuser,
        )
        self.complete_3_5.completed = True
        self.complete_3_5.save()

        mar17_todo = create_todo(
            new_title="March 17th todo",
            new_duedate=datetime.datetime(2020, 3, 17, 14, 0),
            new_course=self.course.id,
            new_ec=self.ec.id,
            user=testuser,
        )

    def test_check_no_todos(self):
        response = self.client.get('/day/2020/mar/12/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have no to-do items for this day!")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_check_one_todo(self):
        response = self.client.get('/day/2020/mar/17/')
        self.assertEqual(response.status_code, 200)

        qs = response.get_queryset(self)
        self.assertEqual(qs, ['<ToDoItem: March 17th todo 2020-03-17>'])
        self.assertContains(response, "March 17th todo")
        self.assertQuerysetEqual(response.context['object_list'], [
                                 '<ToDoItem: March 17th todo 2020-03-17>'])

    def test_check_only_incomplete_todo(self):
        response = self.client.get('/day/2020/mar/5/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "March 5th todo")
        self.assertNotContains(response, "March 5th todo completed")
        self.assertQuerysetEqual(response.context['object_list'], [
                                 '<ToDoItem: March 5th todo 2020-03-05>'])


class TodayViewTest(TestCase):
    def setUp(self):
        #Forces a login to occur, creates a test user if one does not exist
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

        self.course = create_course(new_course_name="Tester")
        self.ec = create_ec(new_name='ec')

        create_todo(
            new_title="Today's todo",
            new_duedate=datetime.date.today(),
            new_completed=False,
            new_course=self.course.id,
            new_ec=self.ec.id,
        )
        
        self.complete_today = create_todo(
            new_title="Today's todo completed",
            new_duedate=datetime.date.today(),
            new_course=self.course.id,
            new_ec=self.ec.id,
        )
        self.complete_today.completed = True
        self.complete_today.save()

        tom_todo = create_todo(
            new_title="Tomorrow's todo",
            new_duedate=datetime.date.today() + datetime.timedelta(days=1),
            new_course=self.course.id,
            new_ec=self.ec.id,
        )

    def test_check_only_today_incomplete_appears(self):
        response = self.client.get('/today/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Today's todo")
        self.assertNotContains(response, "Today's todo completed")



#class WeekViewTest(TestCase):


class MonthViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.force_login(
            User.objects.get_or_create(username='testuser')[0])

        self.course = create_course(new_course_name="Tester")
        self.ec = create_ec(new_name="ec")

        for i in range(1, 11):
            title = "April {} Todo".format(i)
            create_todo(
                new_title=title,
                new_duedate=datetime.datetime(2020, 4, i),
                new_course=self.course.id,
                new_ec=self.ec.id,
            )

        for i in range(1, 6):
            title = "May {} Todo".format(i)
            create_todo(
                new_title=title,
                new_duedate=datetime.datetime(2020, 5, i),
                new_course=self.course.id,
                new_ec=self.ec.id,
            )

    def test_april_todos(self):
        response = self.client.get('/month/2020/Apr/')
        self.assertContains(response, "April")
        self.assertEqual(len(response.context['object_list']), 10)

    def test_may_todos(self):
        response = self.client.get('/month/2020/May/')
        self.assertContains(response, "May")
        self.assertEqual(len(response.context['object_list']), 5)

    # Should be no todos for this month
    def test_month_no_todos(self):
        response = self.client.get('/month/2020/Jan/')
        self.assertContains(response, "January")
        self.assertEqual(len(response.context['object_list']), 0)
"""


class CalendarMonthViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user", email="test_user@mail.site", password="test_password")
        self.client.login(username="test_user", password="test_password")

    def test_april_calendar_view(self):
        response = self.client.get("/month/2020/Apr/")
        self.assertContains(response, "April")

    # def test_next_month(self):
    #     response = self.client.get("/month/2020/Nov/")
    #     self.assertContains(response, "November 2020")
    #     response = self.client.get("/next_month/2020/Nov/")
    #     print(response['location'])
    #     self.assertContains(response, "December 2020")
    #     response = self.client.get("/next_month/2020/Dec/")
    #     print(response['location'])
    #     self.assertContains(response, "January 2021")

    # def test_prev_month(self):
    #     response = self.client.get("/month/2020/Feb/")
    #     self.assertContains(response, "February 2020")
    #     response = self.client.get("/prev_month/2020/Feb/")
    #     print(response['location'])
    #     self.assertContains(response, "January 2020")
    #     response = self.client.get("/prev_month/2020/Jan/")
    #     print(response['location'])
    #     self.assertContains(response, "December 2019")


class TodoListViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Forces a login to occur, creates a test user if one does not exist
        self.client.force_login(
            User.objects.get_or_create(username='testuser')[0])

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo_list:todo_list'))
        self.assertEqual(response.status_code, 200)
        # this view doesn't have a context object...it only has context_data


class ToDoItemFormTest(TestCase):
    """
    Test whether CreateView is successful
    """

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="test_user", email="test_user@mail.site", password="test_password")
        self.user2 = User.objects.create_user(
            username="test_user2", email="test_user@mail.site", password="test_password")
        self.course1 = create_course(new_course_name="Test1", user=self.user1)
        self.course2 = create_course(new_course_name="Test2", user=self.user2)
        self.ec1 = create_ec(new_name='fun1', user=self.user1)
        self.ec2 = create_ec(new_name='fun2', user=self.user2)

        # this data will be passed into the Forms and create/update object
        self.data_form = {
            'title': "TBD",
            'description': '',
            'duedate': timezone.now(),
            'location': '',
            'recur_freq': 'NEVER',
            'end_recur_date': timezone.now(),
            'priority': 'LO',
            'category': 'NN',
            'course': self.course2.id,
            'ec': self.ec2.id,
            'progress': 0,
        }

    def test_todoitemform_success_submission(self):
        self.data_form['title'] = 'Test submission success'
        form = ToDoForm(data=self.data_form)
        self.assertTrue(form.is_valid())

    def test_correct_template_for_add_todo(self):
        self.data_form['title'] = "Test correct template used"
        self.client.force_login(self.user2)
        response = self.client.post(
            reverse('todo_list:add_todo_item'), self.data_form)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todoitem_form.html')

    def test_only_users_courses_in_form(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('todo_list:add_todo_item'))
        print(response.context)
        self.assertEquals(self.user1, response.context['user'])
        self.assertEquals(
            self.course1, response.context['form'].fields['course'].queryset[0])
        self.assertEquals(
            self.ec1, response.context['form'].fields['ec'].queryset[0])


class CreateDailyRecurrencesTest(TestCase):
    def setUp(self):
        self.my_course = create_course(
            new_course_name="Tester"
        )
        self.my_ec = create_ec(new_name='fun')

        # Forces a login to occur, creates a test user if one does not exist
        self.client.force_login(
            User.objects.get_or_create(username='testuser')[0])

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
            'progress': 0,
        }

    def test_create_daily_recurrences_equiv(self):  # equivalence test
        """
        Tests whether create_recurrenes work
        """
        self.data_form['title'] = "Test creating daily recurrences"
        self.data_form['description'] = "Some end_recur_date at the same time"
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 3, 19, 5, 0, 0, tzinfo=pytz.utc)

        daily_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 4 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={
                         'todo_item_id': daily_occurrence.id}), self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(4, len(current_query_set))

        # check crucial fields
        filtered = ToDoItem.objects.filter(title='Test creating daily recurrences',
                                           description="Some end_recur_date at the same time",
                                           recur_freq='DAILY',
                                           end_recur_date=datetime.datetime(2020, 3, 19, 5, 0, 0, tzinfo=pytz.utc))
        self.assertEqual(4, len(filtered))

        count_true = 0
        # check due date
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i+1].duedate - datetime.timedelta(days=1):
                count_true += 1

        # count_true has to be 3 because 3 comparisons if test works
        self.assertEqual(3, count_true)

    def test_redirect_from_create_recurrences_to_todo_list(self):
        """
        Test that after a successful create_recurrences, it redirects to todo_list
        """
        self.data_form['title'] = "Test redirect to list after creating_recurrences"
        self.data_form['recur_freq'] = 'DAILY'
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 3, 31, 5, 0, 0, tzinfo=pytz.utc)
        daily_occurrence = create_from_data_dict(self.data_form)

        response = self.client.post(
            reverse('todo_list:create_recurrences', kwargs={'todo_item_id': daily_occurrence.id}), self.data_form)
        self.assertRedirects(response, reverse('todo_list:todo_list'))

    def test_create_daily_recurrences_shorter_time(self):  # boundary test
        """
        Some end_recur_date not a full day from duedate
        """
        self.data_form['title'] = "Test creating daily recurrences"
        self.data_form['description'] = "Some end_recur_date but with an earlier time than duedate"
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 3, 19, 4, 0, 0, tzinfo=pytz.utc)

        daily_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 3 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={
                         'todo_item_id': daily_occurrence.id}), self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(3, len(current_query_set))

        # check crucial fields
        filtered = ToDoItem.objects.filter(title='Test creating daily recurrences',
                                           description="Some end_recur_date but with an earlier time than duedate",
                                           recur_freq='DAILY',
                                           end_recur_date=datetime.datetime(2020, 3, 19, 4, 0, 0, tzinfo=pytz.utc)).order_by('duedate')
        self.assertEqual(3, len(filtered))

        # check duedates of all 3 objects
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
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 3, 14, 4, 0, 0, tzinfo=pytz.utc)

        daily_occurrence = create_from_data_dict(
            self.data_form)  # create first instance
        # should create 1 instance
        self.client.post(reverse('todo_list:create_recurrences', kwargs={
                         'todo_item_id': daily_occurrence.id}), self.data_form)
        current_instance = ToDoItem.objects.get(
            description="Some end_recur_date earlier than duedate")
        all_instances = [current_instance]

        self.assertEqual(1, len(all_instances))

        # check crucial fields
        one_instance = ToDoItem.objects.get(title="Test creating daily recurrences",
                                            description="Some end_recur_date earlier than duedate",
                                            end_recur_date=datetime.datetime(2020, 3, 14, 4, 0, 0, tzinfo=pytz.utc))

        # check duedates of all 1 object
        self.assertEqual(one_instance.duedate, datetime.datetime(
            2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc))

    def tearDown(self):
        del self.data_form
        del self.my_course
        del self.my_ec


class CreateWeeklyRecurrencesTests(TestCase):
    def setUp(self):
        self.my_course = create_course(
            new_course_name="Tester"
        )

        # Forces a login to occur, creates a test user if one does not exist
        self.client.force_login(
            User.objects.get_or_create(username='testuser')[0])

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
            'course': self.my_course.id,
            'ec': self.my_ec.id,
            'progress': 0
        }

    def test_create_weekly_recurrences_equiv(self):  # equivalence test
        """
        Equivalence Tests for creating weekly recurrences
        """
        self.data_form['end_recur_date'] = datetime.datetime(2020, 4, 6, 5, 0, 0,
                                                             tzinfo=pytz.utc)

        weekly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 4 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': weekly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(4, len(current_query_set))

        # check crucial fields
        filtered = ToDoItem.objects.filter(title="Test creating weekly recurrences equivalence",
                                           recur_freq='WEEKLY',
                                           end_recur_date=datetime.datetime(2020, 4, 6, 5, 0, 0, tzinfo=pytz.utc)).order_by('duedate')
        self.assertEqual(4, len(filtered))

        # check duedates of all 4 objects
        count_true = 0
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(weeks=1):
                count_true += 1

        # count_true has to be 3 because 3 comparisons if test works
        self.assertEqual(3, count_true)

    ################## boundary tests ######################
    def test_create_less_than_a_full_week(self):
        """
        end_recur_date is not a full 4 weeks --> should create only 3 instances
        """
        self.data_form['title'] = "Test creating weekly recurrences boundaries"
        self.data_form['description'] = "end_recur_date is not a full 4 weeks"
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 4, 5, 5, 0, 0, tzinfo=pytz.utc)

        weekly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 3 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': weekly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(3, len(current_query_set))

        # check crucial fields
        filtered = ToDoItem.objects.filter(title="Test creating weekly recurrences boundaries",
                                           description="end_recur_date is not a full 4 weeks",
                                           recur_freq='WEEKLY',
                                           end_recur_date=datetime.datetime(
                                               2020, 4, 5, 5, 0, 0, tzinfo=pytz.utc)
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
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 4, 8, 5, 0, 0, tzinfo=pytz.utc)

        weekly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

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
                                           end_recur_date=datetime.datetime(
                                               2020, 4, 8, 5, 0, 0, tzinfo=pytz.utc)
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
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 4, 5, 3, 0, 0, tzinfo=pytz.utc)

        weekly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 3 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': weekly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(3, len(current_query_set))

        # check crucial fields
        filtered = ToDoItem.objects.filter(title="Test creating weekly recurrences boundaries",
                                           description="end_recur_date is 4 weeks by day but not 4 weeks by time",
                                           recur_freq='WEEKLY',
                                           end_recur_date=datetime.datetime(
                                               2020, 4, 5, 3, 0, 0, tzinfo=pytz.utc)
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
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 3, 10, 4, 0, 0, tzinfo=pytz.utc)

        weekly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance
        # print( daily_occurrence.id )
        # should create 1 instance
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': weekly_occurrence.id}),
                         self.data_form)
        current_instance = ToDoItem.objects.get(
            description="Some end_recur_date earlier than duedate")
        all_instances = [current_instance]

        self.assertEqual(1, len(all_instances))

        # check crucial fields
        one_instance = ToDoItem.objects.get(title="Test creating weekly recurrences",
                                            description="Some end_recur_date earlier than duedate",
                                            end_recur_date=datetime.datetime(2020, 3, 10, 4, 0, 0, tzinfo=pytz.utc))

        # check duedates of  1 object
        self.assertEqual(one_instance.duedate, datetime.datetime(
            2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc))

    def tearDown(self):
        del self.data_form
        del self.my_course
        del self.my_ec


class CreateMonthlyRecurrencesTests(TestCase):
    def setUp(self):
        self.my_course = create_course(
            new_course_name="Tester"
        )

        # Forces a login to occur, creates a test user if one does not exist
        self.client.force_login(
            User.objects.get_or_create(username='testuser')[0])

        self.my_ec = create_ec(new_name='fun')

        # this data will be passed into the Forms and create/update object
        self.data_form = {
            'title': "Test creating monthly recurrences",
            'description': '',
            'duedate': datetime.datetime(2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc),
            'location': '',
            'recur_freq': 'MONTHLY',
            'end_recur_date': datetime.datetime(2020, 6, 16, 5, 0, 0, tzinfo=pytz.utc),
            'priority': 'LO',
            'category': 'NN',
            'course': self.my_course.id,
            'ec': self.my_ec.id,
            'progress': 0
        }

    def test_create_monthly_recurrences_equiv(self):  # equivalence test
        """
        Equivalence Tests for creating 4 monthly recurrences
        """
        monthly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 4 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': monthly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(4, len(current_query_set))

        # check crucial fields
        filtered = ToDoItem.objects.filter(title="Test creating monthly recurrences",
                                           recur_freq='MONTHLY',
                                           end_recur_date=datetime.datetime(2020, 6, 16, 5, 0, 0, tzinfo=pytz.utc)).order_by('duedate')
        self.assertEqual(4, len(filtered))

        # check duedates of all 4 objects
        count_true = 0
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(months=1):
                count_true += 1

        # count_true has to be 3 because 3 comparisons if test works
        self.assertEqual(3, count_true)

    ################## boundary tests ######################
    def test_create_less_than_a_full_month_date(self):
        """
        end_recur_date is not a full 4 months --> should create only 3 instances
        """
        self.data_form['title'] = "Test creating monthly recurrences boundaries"
        self.data_form['description'] = "end_recur_date is not a full 4 months by dates"
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 5, 16, 5, 0, 0, tzinfo=pytz.utc)

        weekly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 3 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': weekly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(3, len(current_query_set))

        # check crucial fields
        # check titles
        filtered = ToDoItem.objects.filter(title="Test creating monthly recurrences boundaries",
                                           description="end_recur_date is not a full 4 months by dates",
                                           recur_freq='MONTHLY',
                                           end_recur_date=datetime.datetime(
                                               2020, 5, 16, 5, 0, 0, tzinfo=pytz.utc)
                                           ).order_by('duedate')
        self.assertEqual(3, len(filtered))

        # check duedates of all 3 objects
        count_true = 0
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(months=1):
                count_true += 1

        # count_true has to be 2 because 2 comparisons if test works
        self.assertEqual(2, count_true)

    def test_create_less_than_a_full_month_time(self):
        """
        end_recur_date is not a full 4 months by time --> should create only 3 instances
        """
        self.data_form['title'] = "Test creating monthly recurrences boundaries"
        self.data_form['description'] = "end_recur_date is not a full 4 months by time"
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 5, 16, 4, 0, 0, tzinfo=pytz.utc)

        monthly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 3 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': monthly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(3, len(current_query_set))

        # check crucial fields
        filtered = ToDoItem.objects.filter(title="Test creating monthly recurrences boundaries",
                                           description="end_recur_date is not a full 4 months by time",
                                           recur_freq='MONTHLY',
                                           end_recur_date=datetime.datetime(
                                               2020, 5, 16, 4, 0, 0, tzinfo=pytz.utc)
                                           ).order_by('duedate')
        self.assertEqual(3, len(filtered))

        # check duedates of all 3 objects
        count_true = 0
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(months=1):
                count_true += 1

        # count_true has to be 3 because 3 comparisons if test works
        self.assertEqual(2, count_true)

    def test_create_more_than_a_full_month_dates(self):
        """
        end_recur_date is more than a full 4 month --> should create 4 instances
        """
        self.data_form['title'] = "Test creating monthly recurrences boundaries"
        self.data_form['description'] = "end_recur_date is more than 4 months but less than 5 months by dates"
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 6, 30, 5, 0, 0, tzinfo=pytz.utc)

        monthly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 4 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': monthly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(4, len(current_query_set))

        # check crucial fields
        # check titles
        filtered = ToDoItem.objects.filter(title="Test creating monthly recurrences boundaries",
                                           description="end_recur_date is more than 4 months but less than 5 months by dates",
                                           recur_freq='MONTHLY',
                                           end_recur_date=datetime.datetime(
                                               2020, 6, 30, 5, 0, 0, tzinfo=pytz.utc)
                                           ).order_by('duedate')
        self.assertEqual(4, len(filtered))

        # check duedates of all 4 objects
        count_true = 0
        # check due date
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(months=1):
                count_true += 1

        # count_true has to be 3 because 3 comparisons if test works
        self.assertEqual(3, count_true)

    def test_create_more_than_a_full_month_time(self):
        """
        end_recur_date is more than a full 4 months --> should create 4 instances
        """
        self.data_form['title'] = "Test creating monthly recurrences boundaries"
        self.data_form['description'] = "end_recur_date is more than 4 months but less than 5 months by time"
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 6, 16, 5, 1, 0, tzinfo=pytz.utc)

        monthly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 4 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': monthly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(4, len(current_query_set))

        # check crucial fields
        filtered = ToDoItem.objects.filter(title="Test creating monthly recurrences boundaries",
                                           description="end_recur_date is more than 4 months but less than 5 months by time",
                                           recur_freq='MONTHLY',
                                           end_recur_date=datetime.datetime(
                                               2020, 6, 16, 5, 1, 0, tzinfo=pytz.utc)
                                           ).order_by('duedate')
        self.assertEqual(4, len(filtered))

        # check duedates of all 4 objects
        count_true = 0
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(months=1):
                count_true += 1

        # count_true has to be 3 because 3 comparisons if test works
        self.assertEqual(3, count_true)

    def test_end_date_earlier_than_duedate_month(self):  # edge case
        """
        Create end_recur_date earlier than duedate --> should create only one instance

        """
        self.data_form['title'] = "Test creating monthly recurrences"
        self.data_form['description'] = "Some end_recur_date earlier than duedate by month and time"
        self.data_form['end_recur_date'] = datetime.datetime(
            2020, 2, 10, 4, 0, 0, tzinfo=pytz.utc)

        yearly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 1 instance
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': yearly_occurrence.id}),
                         self.data_form)
        current_instance = ToDoItem.objects.get(
            description="Some end_recur_date earlier than duedate by month and time")
        all_instances = [current_instance]

        self.assertEqual(1, len(all_instances))

        # check crucial fields

        one_instance = ToDoItem.objects.get(title="Test creating monthly recurrences",
                                            description="Some end_recur_date earlier than duedate by month and time",
                                            end_recur_date=datetime.datetime(2020, 2, 10, 4, 0, 0, tzinfo=pytz.utc))

        # check duedates of  1 object
        self.assertEqual(one_instance.duedate, datetime.datetime(
            2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc))


class CreateYearlyRecurrencesTests(TestCase):
    def setUp(self):
        self.my_course = create_course(
            new_course_name="Tester"
        )

        # Forces a login to occur, creates a test user if one does not exist
        self.client.force_login(
            User.objects.get_or_create(username='testuser')[0])

        self.my_ec = create_ec(new_name='fun')

        # this data will be passed into the Forms and create/update object
        self.data_form = {
            'title': "Test creating yearly recurrences",
            'description': '',
            'duedate': datetime.datetime(2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc),
            'location': '',
            'recur_freq': 'YEARLY',
            'end_recur_date': datetime.datetime(2023, 3, 16, 5, 0, 0, tzinfo=pytz.utc),
            'priority': 'LO',
            'category': 'NN',
            'course': self.my_course.id,
            'ec': self.my_ec.id,
            'progress': 0
        }

    def test_create_yearly_recurrences_equiv(self):  # equivalence test
        """
        Equivalence Tests for creating 4 yearly recurrences
        """
        yearly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 4 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': yearly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(4, len(current_query_set))

        # check crucial fields
        filtered = ToDoItem.objects.filter(title="Test creating yearly recurrences",
                                           recur_freq='YEARLY',
                                           end_recur_date=datetime.datetime(2023, 3, 16, 5, 0, 0, tzinfo=pytz.utc)).order_by('duedate')
        self.assertEqual(4, len(filtered))

        # check duedates of all 4 objects
        count_true = 0
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(years=1):
                count_true += 1

        # count_true has to be 3 because 3 comparisons if test works
        self.assertEqual(3, count_true)

    ################## boundary tests ######################
    def test_create_less_than_a_full_year_dates(self):
        """
        end_recur_date is not a full 4 years --> should create only 3 instances
        """
        self.data_form['title'] = "Test creating yearly recurrences boundaries"
        self.data_form['description'] = "end_recur_date is not a full 4 years by dates"
        self.data_form['end_recur_date'] = datetime.datetime(
            2023, 2, 16, 5, 0, 0, tzinfo=pytz.utc)

        yearly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 3 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': yearly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(3, len(current_query_set))

        # check crucial fields
        # check titles
        filtered = ToDoItem.objects.filter(title="Test creating yearly recurrences boundaries",
                                           description="end_recur_date is not a full 4 years by dates",
                                           recur_freq='YEARLY',
                                           end_recur_date=datetime.datetime(
                                               2023, 2, 16, 5, 0, 0, tzinfo=pytz.utc)
                                           ).order_by('duedate')
        self.assertEqual(3, len(filtered))

        # check duedates of all 3 objects
        count_true = 0
        # check due date
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(years=1):
                count_true += 1

        # count_true has to be 2 because 2 comparisons if test works
        self.assertEqual(2, count_true)

    def test_create_less_than_a_full_year_time(self):
        """
        end_recur_date is not a full 4 years but only by time --> should create only 4 instances
        """
        self.data_form['title'] = "Test creating yearly recurrences boundaries"
        self.data_form['description'] = "end_recur_date is not a full 4 years by time"
        self.data_form['end_recur_date'] = datetime.datetime(
            2023, 3, 16, 4, 0, 0, tzinfo=pytz.utc)

        yearly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 3 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': yearly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()

        self.assertEqual(3, len(current_query_set))

        # check crucial fields
        # check titles
        filtered = ToDoItem.objects.filter(title="Test creating yearly recurrences boundaries",
                                           description="end_recur_date is not a full 4 years by time",
                                           recur_freq='YEARLY',
                                           end_recur_date=datetime.datetime(
                                               2023, 3, 16, 4, 0, 0, tzinfo=pytz.utc)
                                           ).order_by('duedate').order_by('duedate')
        self.assertEqual(3, len(filtered))

        # check duedates of all 3 objects
        count_true = 0
        # check due date
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(years=1):
                count_true += 1

        # count_true has to be 2 because 2 comparisons if test works
        self.assertEqual(2, count_true)

    def test_create_more_than_a_full_year_dates(self):
        """
        end_recur_date is more than a full 4 years --> should create 4 instances
        """
        self.data_form['title'] = "Test creating yearly recurrences boundaries"
        self.data_form['description'] = "end_recur_date is more than 4 years but less than 5 years by dates"
        self.data_form['end_recur_date'] = datetime.datetime(
            2023, 4, 30, 5, 0, 0, tzinfo=pytz.utc)

        yearly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 4 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': yearly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()

        self.assertEqual(4, len(current_query_set))

        # check crucial fields
        # check titles
        filtered = ToDoItem.objects.filter(title="Test creating yearly recurrences boundaries",
                                           description="end_recur_date is more than 4 years but less than 5 years by dates",
                                           recur_freq='YEARLY',
                                           end_recur_date=datetime.datetime(
                                               2023, 4, 30, 5, 0, 0, tzinfo=pytz.utc)
                                           ).order_by('duedate')
        self.assertEqual(4, len(filtered))

        # check duedates of all 4 objects
        count_true = 0
        # check due date
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(years=1):
                count_true += 1

        # count_true has to be 3 because 3 comparisons if test works
        self.assertEqual(3, count_true)

    def test_create_more_than_a_full_year_time(self):
        """
        end_recur_date is not a full 4 years --> should create 4 instances
        """
        self.data_form['title'] = "Test creating yearly recurrences boundaries"
        self.data_form['description'] = "end_recur_date is more than 4 years but less than 5 years by time"
        self.data_form['end_recur_date'] = datetime.datetime(
            2023, 3, 16, 6, 0, 0, tzinfo=pytz.utc)

        yearly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        # should create 4 instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': yearly_occurrence.id}),
                         self.data_form)
        current_query_set = ToDoItem.objects.all()
        self.assertEqual(4, len(current_query_set))

        # check crucial fields
        # check titles
        filtered = ToDoItem.objects.filter(title="Test creating yearly recurrences boundaries",
                                           description="end_recur_date is more than 4 years but less than 5 years by time",
                                           recur_freq='YEARLY',
                                           end_recur_date=datetime.datetime(
                                               2023, 3, 16, 6, 0, 0, tzinfo=pytz.utc)
                                           ).order_by('duedate')

        self.assertEqual(4, len(filtered))

        # check duedates of all 4 objects
        count_true = 0
        # check due date
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(years=1):
                count_true += 1

        # count_true has to be 3 because 3 comparisons if test works
        self.assertEqual(3, count_true)

    def test_end_date_earlier_than_duedate_year(self):  # edge case
        """
        Create end_recur_date earlier than duedate --> should create only one instance
        """
        self.data_form['title'] = "Test creating yearly recurrences"
        self.data_form['description'] = "Some end_recur_date earlier than duedate by year"
        self.data_form['end_recur_date'] = datetime.datetime(
            2019, 2, 10, 4, 0, 0, tzinfo=pytz.utc)

        yearly_occurrence = create_from_data_dict(
            self.data_form)  # create first instance

        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': yearly_occurrence.id}),
                         self.data_form)
        current_instance = ToDoItem.objects.get(
            description="Some end_recur_date earlier than duedate by year")
        all_instances = [current_instance]

        self.assertEqual(1, len(all_instances))

        # check crucial fields
        one_instance = ToDoItem.objects.get(title="Test creating yearly recurrences",
                                            description="Some end_recur_date earlier than duedate by year",
                                            recur_freq='YEARLY',
                                            end_recur_date=datetime.datetime(2019, 2, 10, 4, 0, 0, tzinfo=pytz.utc))
        # check duedates of  1 object
        self.assertEqual(one_instance.duedate, datetime.datetime(
            2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc))


class UpdateViewTest(TestCase):
    def setUp(self):
        self.my_course = create_course(
            new_course_name="Tester"
        )
        self.my_ec = create_ec(new_name='fun')

        # Forces a login to occur, creates a test user if one does not exist
        self.client.force_login(
            User.objects.get_or_create(username='testuser')[0])

        self.data_form = {
            'title': "TBD",
            'description': '',
            'duedate': datetime.datetime(2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc),
            'location': '',
            'recur_freq': 'DAILY',
            'end_recur_date': datetime.datetime(2020, 3, 19, 5, 0, 0, tzinfo=pytz.utc),
            'priority': 'LO',
            'category': 'NN',
            'course': self.my_course.id,
            'ec': self.my_ec.id,
            'progress': 0
        }

    def test_correct_template_for_updateview(self):
        daily_occurrence = create_from_data_dict(self.data_form)
        response = self.client.post(reverse('todo_list:detail', kwargs={'pk': daily_occurrence.id}),
                                    self.data_form)
        self.assertTemplateUsed(response, 'todo/edit_todoitem_form.html')

    def test_edit_todoitemform_success_submission(self):
        self.data_form['title'] = 'Change submit'
        form = ToDoForm(data=self.data_form)
        self.assertTrue(form.is_valid())

    def test_change_all_todo_titles_only(self):
        daily_occurrence = create_from_data_dict(self.data_form)

        # create instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': daily_occurrence.id}),
                         self.data_form)

        # Change fields: hard coded because not going through UpdateView first
        first = ToDoItem.objects.get(pk=daily_occurrence.id)
        first.title = "Changed titles successful"
        first.has_title_changed = True

        for todo in ToDoItem.objects.filter(duedate__gt=first.duedate):
            first.future_events.append(todo.id)

        first.save()

        # change all
        self.client.post(reverse('todo_list:change_all', kwargs={'todo_item_id': first.id}),
                         self.data_form)
        current_query = ToDoItem.objects.filter(
            title="Changed titles successful")
        # there should be 4 instances

        self.assertEqual(4, len(current_query))

    def test_change_all_todo_descriptions_only(self):
        daily_occurrence = create_from_data_dict(self.data_form)
        # create instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': daily_occurrence.id}),
                         self.data_form)

        # Change fields: hard coded because not going through UpdateView first
        second = ToDoItem.objects.get(pk=daily_occurrence.id+1)
        second.description = "Changed description for 3/4 successfully"
        second.has_description_changed = True

        for todo in ToDoItem.objects.filter(duedate__gt=second.duedate):
            second.future_events.append(todo.id)

        second.save()
        # change all
        self.client.post(reverse('todo_list:change_all', kwargs={'todo_item_id': second.id}),
                         self.data_form)
        current_query = ToDoItem.objects.filter(
            description="Changed description for 3/4 successfully")
        # there should be 3 instances
        self.assertEqual(3, len(current_query))

    def test_change_all_todo_titles_and_descr(self):
        daily_occurrence = create_from_data_dict(self.data_form)
        # create instances
        self.client.post(reverse('todo_list:create_recurrences', kwargs={'todo_item_id': daily_occurrence.id}),
                         self.data_form)

        # Change fields: hard coded because not going through UpdateView first
        third = ToDoItem.objects.get(pk=daily_occurrence.id+2)
        third.title = "Title changed"
        third.description = "Changed description for 2 of the last ones in the list successfully"
        third.has_title_changed = True
        third.has_description_changed = True

        for todo in ToDoItem.objects.filter(duedate__gt=third.duedate):
            third.future_events.append(todo.id)
        third.save()

        # change all
        self.client.post(reverse('todo_list:change_all', kwargs={'todo_item_id': third.id}),
                         self.data_form)

        current_query = ToDoItem.objects.filter(title="Title changed",
                                                description="Changed description for 2 of the last ones in the list successfully")

        # there should be 2 instances
        self.assertEqual(2, len(current_query))


class TestEditRecurrences(TestCase):
    def setUp(self):
        self.my_course = create_course(
            new_course_name="Tester"
        )

        # Forces a login to occur, creates a test user if one does not exist
        self.client.force_login(
            User.objects.get_or_create(username='testuser')[0])

        self.my_ec = create_ec(new_name='fun')
        self.data_form = {
            'title': "Test edit recurrences",
            'description': '',
            'duedate': datetime.datetime(2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc),
            'location': '',
            'recur_freq': 'NEVER',
            'end_recur_date': datetime.datetime(2020, 3, 30, 5, 0, 0, tzinfo=pytz.utc),
            'priority': 'LO',
            'category': 'NN',
            'course': self.my_course.id,
            'ec': self.my_ec.id,
            'progress': 0
        }

    def test_changing_duedate_only_to_later(self):
        self.data_form['title'] = "Test redirect to edit_recurrences"
        self.data_form['recur_freq'] = 'DAILY'  # create 15 instances
        daily_occurrence = create_from_data_dict(self.data_form)
        response = self.client.post(reverse('todo_list:create_recurrences', kwargs={
                                    'todo_item_id': daily_occurrence.id}), self.data_form)
        current_query_before_change = ToDoItem.objects.all()
        self.assertEqual(15, len(current_query_before_change))

        # check fields
        filtered = ToDoItem.objects.filter(title="Test redirect to edit_recurrences",
                                           duedate__gte=datetime.datetime(
                                               2020, 3, 16, 5, 0, 0, tzinfo=pytz.utc),
                                           recur_freq='DAILY',
                                           end_recur_date=datetime.datetime(2020, 3, 30, 5, 0, 0, tzinfo=pytz.utc)).order_by('duedate')
        self.assertEqual(15, len(filtered))

        count_true = 0
        for i in range(len(filtered) - 1):
            if filtered[i].duedate == filtered[i + 1].duedate - relativedelta(days=1):
                count_true += 1

        # count_true has to be 15 because 15 comparisons if test works
        self.assertEqual(14, count_true)

        first = ToDoItem.objects.get(pk=daily_occurrence.id)
        # should create 15 instances because one of the instances is deleted
        first.duedate = datetime.datetime(
            2020, 3, 19, 5, 0, 0, tzinfo=pytz.utc)
        first.has_duedate_changed = True
        first.save()

        self.client.post(reverse('todo_list:edit_recurrences', kwargs={
                         'todo_item_id': first.id}), self.data_form)
        current_query = ToDoItem.objects.all()

        self.assertEqual(15, len(current_query))

    def tearDown(self):
        del self.data_form
        del self.my_course
        del self.my_ec


class TestNotes(TestCase):
    def setUp(self):
        self.user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(self.user)
        self.note = Note.objects.create(user=self.user, text='test note')

    def test_todolist_context(self):
        response = self.client.get(reverse('todo_list:todo_list'))
        self.assertEqual(response.context['note'], self.note.text)

    def test_createnote_post(self):
        response = self.client.post(reverse('todo_list:notes'), {
                                    'user': self.user, 'notes-text': self.note.text})
        # redirects to the todo list
        self.assertEqual(response.status_code, 302)
