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
]