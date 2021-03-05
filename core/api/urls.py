from django.urls import path

from . import views

# app_name = 'core'

urlpatterns = [
    path('', views.TODO.as_view(), name='list-display'),
]