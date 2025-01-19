from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('delete/<str:model_name>/<int:pk>/', views.delete_record, name='delete_record'),
]