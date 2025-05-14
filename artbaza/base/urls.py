from django.urls import path
from . import views


urlpatterns = [
    path('artwork_detailed/<int:pk>/', views.artwork_detailed, name='base_artwork_detailed'),
    path('', views.index, name='base_index'),
]


