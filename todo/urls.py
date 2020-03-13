from django.urls import path

from . import views

app_name = 'todo_list'
urlpatterns = [
    path('', views.ToDoListView.as_view(), name='todo_list'),
    path('<int:pk>/', views.EditToDo.as_view(), name='detail' ),
    path('completed/', views.CompletedView.as_view(), name='completed'),
    path('<int:todo_item_id>/complete_todo/', views.completeToDo, name="complete_todo"),
    path('add_todo_item/', views.AddToDoItemView.as_view(), name='add_todo_item'),
    path('delete_todo_item/<int:todo_item_id>/', views.delete_todo, name='delete_todo_item'),
    path('<int:todo_item_id>/change_all/', views.change_all, name='change_all'),
    path('add_todo_item/<int:todo_item_id>/create_recurrences/', views.create_recurrences, name='create_recurrences'),
    path('<int:todo_item_id>/edit_recurrences/', views.edit_recurrences, name='edit_recurrences' ),

    # path('academics/', views.AcademicsListView.as_view(), name='academics_list'),
    # path('extracurriculars/', views.ECListView.as_view(), name='ec_list'),
    # path('job/', views.JobListView.as_view(), name='job_list'),
    # path('social/', views.SocialListView.as_view(), name='social_list'),
    # path('personal/', views.PersonalListView.as_view(), name='personal_list'),
    # path('other/', views.OtherListView.as_view(), name='other_list'),

    path('your_specifics/', views.SpecificListView.as_view(), name= 'specific_list'),
    path('add_specific/', views.AddSpecificView.as_view(), name='add_specific'),
    path('<int:pk>/edit_specific/', views.EditSpecificView.as_view(), name='edit_specific'),
    path('<int:sp_id>/delete_specific/', views.delete_specific, name='delete_specific'),

    path('your_categories/', views.CategoryListView.as_view(), name= 'category_list'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('<int:pk>/edit_category/', views.EditCategoryView.as_view(), name='edit_category'),
    path('<int:category_id>/delete_category/', views.delete_category, name='delete_category'),

    path('ajax/load-specifics/', views.load_specifics, name='ajax_load_specifics'),




]