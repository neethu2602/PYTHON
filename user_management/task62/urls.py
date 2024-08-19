from django.urls import path
from .views import home,RegisterView
from django.contrib.auth import views as auth_views
from task62.views import CustomLoginView,profile
from task62.forms import LoginForm
from . import views

app_name = 'task62'
urlpatterns = [
    path('', home, name='users-home'),
    path('create_portfolio/', views.create_or_update_portfolio, name='create_portfolio'),

    path('profile/', profile, name='users-profile'),
    path('portfolio/', views.portfolio, name='portfolio_detail'),
    path('projects/', views.projects_page, name='projects_page'),
    path('work/', views.work_experience_page, name='work_experience_page'),
    path('education/', views.education_page, name='education_page'),
    path('certifications/', views.certifications_page, name='certifications_page'),


    path('add_project/', views.add_project, name='add_project'),
    path('edit_project/<int:pk>/', views.edit_project, name='edit_project'),
    path('delete_project/<int:pk>/', views.delete_project, name='delete_project'),
    path('add_work_experience/', views.add_work_experience, name='add_work_experience'),
    path('edit_work_experience/<int:pk>/', views.edit_work_experience, name='edit_work_experience'),
    path('delete_work_experience/<int:pk>/', views.delete_work_experience, name='delete_work_experience'),
    path('add_education/', views.add_education, name='add_education'),
    path('edit_education/<int:pk>/', views.edit_education, name='edit_education'),
    path('delete_education/<int:pk>/', views.delete_education, name='delete_education'),
    path('add_certification/', views.add_certification, name='add_certification'),
    path('edit_certification/<int:pk>/', views.edit_certification, name='edit_certification'),
    path('delete_certification/<int:pk>/', views.delete_certification, name='delete_certification'),






]

