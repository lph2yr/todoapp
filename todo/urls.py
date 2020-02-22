from django.urls import path

from . import views

app_name = 'todo_list'
urlpatterns = [
    path('', views.ToDoListView.as_view(), name='todo_list'),

    #path('<int:todo_item_id>/', views.detail, name='detail' ), #edit view
    #path('<int:pk>/', views.EditToDo.as_view(success_url='/'), name='detail' ), #edit view
    path('<int:todo_item_id>/', views.detail, name='detail' ), #edit view

    path('completed/', views.CompletedView.as_view(), name='completed'),

    path('<int:todo_item_id>/complete_todo', views.completeToDo, name="complete_todo"),

    path('add_todo_item/', views.AddToDoItemView.as_view(success_url='/'), name = 'add_todo_item'),
]