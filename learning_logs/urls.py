"""Определение схемы url для приложения learning_logs"""
from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
        #Домашняя страница
    path('', views.index, name = 'index'),
        #страница со списком всех тем
    path('topics/', views.topics, name = 'topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
        #страница для добавления новой темы
    path('new_topic/', views.new_topic, name='new_topic'),
    # path('index2/', views.index2, name='index2'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete_topic/<int:topic_id>', views.delete_topic, name='delete_topic'),
    path('delete_entry/<int:entry_id>', views.delete_entry, name='delete_entry'),
    
]
