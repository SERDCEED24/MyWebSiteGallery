from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('artwork_detailed/<int:pk>/', views.artwork_detailed, name='artwork_detailed'),
    path('Artwork/', views.index, {'model_name': 'Artwork'}, name='artwork_index'),
    path('Author/', views.index, {'model_name': 'Author'}, name='author_index'),
    path('Genre/', views.index, {'model_name': 'Genre'}, name='genre_index'),
    path('Material/', views.index, {'model_name': 'Material'}, name='material_index'),
    path('Technique/', views.index, {'model_name': 'Technique'}, name='technique_index'),
    path('WorkStatus/', views.index, {'model_name': 'WorkStatus'}, name='workstatus_index'),
    path('delete/<str:model_name>/<int:pk>/', views.delete_record, name='delete_record'),
    path('form/<str:model_name>/<int:pk>/', views.form, name='edit_form'),
    path('form/<str:model_name>/', views.form, name='add_form'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('tree/', views.tree_view, name='tree'),
    path('delete_treenode/<str:model_name>/<int:pk>/', views.delete_treenode, name='delete_treenode'),
    path('delete_multiple/<str:model_name>/', views.delete_multiple, name="delete_multiple"),
]


