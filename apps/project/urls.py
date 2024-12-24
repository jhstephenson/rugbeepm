from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Client URLs
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<uuid:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<uuid:pk>/edit/', views.ClientUpdateView.as_view(), name='client_edit'),

    # Project URLs
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<uuid:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<uuid:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<uuid:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),

    # Project Member URLs
    path('projects/<uuid:project_id>/members/add/', views.ProjectMemberCreateView.as_view(), name='project_member_add'),

    # Task URLs
    path('projects/<uuid:project_id>/tasks/create/', views.TaskCreateView.as_view(), name='project_task_create'),
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<uuid:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<uuid:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<uuid:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('projects/<uuid:project_id>/tasks/<uuid:pk>/time-entries/add/', views.TimeEntryCreateView.as_view(), name='task_timeentry_create'),

    # Time Entry URLs
    path('tasks/<uuid:task_id>/time-entries/create/', views.TimeEntryCreateView.as_view(), name='task_timeentry_create'),
    path('time-entries/add/', views.TimeEntryCreateView.as_view(), name='timeentry_create'),
    path('time-entries/<uuid:pk>/edit/', views.TimeEntryUpdateView.as_view(), name='timeentry_edit'),
    path('time-entries/<uuid:pk>/delete/', views.TimeEntryDeleteView.as_view(), name='timeentry_delete'),

    # Profile and Categories URLs
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<uuid:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<uuid:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<uuid:category_id>/values/create/', views.CategoryValueCreateView.as_view(), name='category_value_create'),
    path('categories/<uuid:category_id>/values/<uuid:value_id>/edit/', views.CategoryValueUpdateView.as_view(), name='category_value_edit'),
]