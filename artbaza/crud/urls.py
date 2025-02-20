from django.urls import path
from . import views


urlpatterns = [
    path('<str:model_name>/', views.index, name='index'),
    path('delete/<str:model_name>/<int:pk>/', views.delete_record, name='delete_record'),
    path('form/<str:model_name>/<int:pk>/', views.form, name='edit_form'),
    path('form/<str:model_name>/', views.form, name='add_form'),
]

