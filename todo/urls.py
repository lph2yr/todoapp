from django.urls import path

from . import views

app_name = 'todo_list'
urlpatterns = [
    path('', views.ToDoListView.as_view(), name='todo_list'),
    path('notes/', views.save_notes, name='notes'),
    path('<int:pk>/', views.EditToDo.as_view(), name='detail'),
    path('completed/', views.CompletedView.as_view(), name='completed'),
    path('<int:todo_item_id>/complete_todo/',
         views.complete_todo, name="complete_todo"),
    path('add_todo_item/', views.AddToDoItemView.as_view(), name='add_todo_item'),
    path('delete_todo_item/<int:todo_item_id>/',
         views.delete_todo, name='delete_todo_item'),
    path('<int:todo_item_id>/change_all/', views.change_all, name='change_all'),
    path('add_todo_item/<int:todo_item_id>/create_recurrences/',
         views.create_recurrences, name='create_recurrences'),

    path('day/', views.DayView.as_view(), name='day'),
    path('day/<int:year>/<str:month>/<int:day>/',
         views.SpecificDayView.as_view(), name='specific_day'),
    path('today/', 
          views.TodoTodayArchiveView.as_view(), name='archive_today'),
    path('<int:todo_item_id>/edit_recurrences/',
         views.edit_recurrences, name='edit_recurrences'),
    path('<int:todo_item_id>/add_subtask/',
         views.create_subtask_model_form, name='add_subtask'),
    path('<int:subtask_id>/complete_subtask/',
         views.complete_subtask, name='complete_subtask'),

    path('week/', views.WeekView.as_view(), name='week'),
    path('<int:year>/week/<int:week>/', views.SpecificWeekView.as_view(), name='specific_week'),

    path('month/', views.MonthView.as_view(), name='month'),
    path('month/<int:year>/<str:month>/', views.month_calendar_view, name='specific_month'),
    path('next_month/<int:year>/<str:month>/', views.month_calendar_next, name='next_month'),
    path('prev_month/<int:year>/<str:month>/', views.month_calendar_prev, name='prev_month'),

    path('job/', views.JobListView.as_view(), name='job_list'),
    path('job/today/', views.JobTodayList.as_view(), name='job_today_todo_list'),
    path('social/', views.SocialListView.as_view(), name='social_list'),
    path('social/today/', views.SocTodayList.as_view(), name='social_today_todo_list'),
    path('personal/', views.PersonalListView.as_view(), name='personal_list'),
    path('personal/today/', views.PersonalTodayList.as_view(), name='personal_today_todo_list'),
    path('other/', views.OtherListView.as_view(), name='other_list'),
    path('other/today/', views.OtherTodayList.as_view(), name='other_today_todo_list'),

    path('academics/', views.AcademicsListView.as_view(), name='academics_list'),
    path('academics/today/', views.AcademicsListTodayView.as_view(), name='academics_today_todo_list'),
    path('add_course/', views.AddCourseView.as_view(), name='add_course'),
    path('your_courses/', views.CourseListView.as_view(), name='course_list'),
    path('course/<int:course_id>/delete_course/',
         views.delete_course, name='delete_course'),
    path('course/<int:pk>/edit_course/',
         views.EditCourseView.as_view(), name='edit_course'),

    path('extracurriculars/', views.ECToDoList.as_view(), name='ec_todo_list'),
    path('extracurriculars/today', views.ECTodayList.as_view(), name='ec_today_todo_list'),
    path('your_ec/', views.ECListView.as_view(), name='ec_list'),
    path('add_ec', views.AddEC.as_view(), name='add_ec'),
    path('ec/<int:pk>/edit_ec/', views.EditEC.as_view(), name='edit_ec'),
    path('ec/<int:ec_id>/delete_ec', views.delete_ec, name='delete_ec'),

    path('delete_all_completed/', views.delete_all_completed,
         name='delete_all_completed'),
    path('delete_all_incompleted/', views.delete_all_incompleted,
         name='delete_all_incompleted'),

]
