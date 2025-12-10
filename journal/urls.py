from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='journal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit/', views.submit_manuscript, name='submit_manuscript'),
    path('assign_reviewer/<int:manuscript_id>/', views.assign_reviewer, name='assign_reviewer'),
    path('submit_review/<int:manuscript_id>/', views.submit_review, name='submit_review'),
    path('make_decision/<int:manuscript_id>/', views.make_decision, name='make_decision'),
    path('publish_article/<int:manuscript_id>/', views.publish_article, name='publish_article'),
    path('issue/<int:issue_id>/', views.issue_detail, name='issue_detail'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('search/', views.search, name='search'),
]
