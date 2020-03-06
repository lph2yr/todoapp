from django.urls import path

from . import views

app_name = 'todo_list'
urlpatterns = [
    path('', views.ToDoListView.as_view(), name='todo_list'),
    path('<int:pk>/', views.EditToDo.as_view(success_url='/'), name='detail' ),
    path('completed/', views.CompletedView.as_view(), name='completed'),
    path('<int:todo_item_id>/complete_todo/', views.completeToDo, name="complete_todo"),
    path('add_todo_item/', views.AddToDoItemView.as_view(), name='add_todo_item'),
    path('delete_todo_item/<int:todo_item_id>/', views.delete_todo, name='delete_todo_item'),
    path('add_todo_item/<int:todo_item_id>/create_recurrences/', views.create_recurrences, name='create_recurrences'),
    path('<int:todo_item_id>/edit_recurrences/', views.edit_recurrences, name='edit_recurrences' ),
    path('academics/', views.AcademicsListView.as_view(), name='academics_list'),
    path('extracurriculars/', views.ECListView.as_view(), name='ec_list'),
    path('job/', views.JobListView.as_view(), name='job_list'),
    path('social/', views.SocialListView.as_view(), name='social_list'),
    path('personal/', views.PersonalListView.as_view(), name='personal_list'),
    path('other/', views.OtherListView.as_view(), name='other_list'),

]