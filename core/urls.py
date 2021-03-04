from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),

    path('create-list/', views.list_create, name='list-create'),

    path('list-detail/<slug:title>/', views.list_detail, name='list-detail'),
    path('list-detail/<slug:title>/change/', views.list_update, name='list-update'),
    path('list-detail/<slug:title>/delete/', views.list_delete, name='list-delete'),
    path('list-detail/<slug:title>/delete-confirm', views.list_delete_confirm, name='list-delete-confirm'),

    path('list-detail/<slug:title>/create-task/', views.task_create, name='task-create'),
    path('list-detail/<slug:title>/<slug:task>/change', views.task_update, name='task-update'),
    path('list-detail/<slug:title>/<slug:task>/delete/', views.task_delete, name='task-delete'),
    path('list-detail/<slug:title>/<slug:task>/delete-confirm/', views.task_delete_confirm, name='task-delete-confirm'),

    path('search/', views.search_list_or_task, name='search'),

]