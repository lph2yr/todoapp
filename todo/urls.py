from django.urls import path

from . import views

app_name = 'todo_list'
urlpatterns = [
    path('', views.ToDoListView.as_view(), name='todo_list'),

    path('<int:todo_item_id>/', views.detail, name='detail' ),

    path('completed/', views.CompletedView.as_view(), name='completed'),

]