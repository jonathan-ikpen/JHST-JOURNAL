from django.urls import path
from . import views
from .forms import UserLoginForm
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='journal/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/manuscript/<int:manuscript_id>/', views.dashboard_manuscript_detail, name='dashboard_manuscript_detail'),
    path('dashboard/my-submissions/', views.my_submissions, name='my_submissions'),
    path('dashboard/my-submissions/<int:manuscript_id>/', views.my_submission_detail, name='my_submission_detail'),
    path('dashboard/review-assignment/<int:manuscript_id>/', views.reviewer_manuscript_detail, name='reviewer_manuscript_detail'),
    path('profile/', views.profile, name='profile'),
    path('submit/', views.submit_manuscript, name='submit_manuscript'),
    path('assign_reviewer/<int:manuscript_id>/', views.assign_reviewer, name='assign_reviewer'),
    path('submit_review/<int:manuscript_id>/', views.submit_review, name='submit_review'),
    path('make_decision/<int:manuscript_id>/', views.make_decision, name='make_decision'),
    path('publish_article/<int:manuscript_id>/', views.publish_article, name='publish_article'),
    path('mark_as_paid/<int:manuscript_id>/', views.mark_as_paid, name='mark_as_paid'),
    path('create_issue/', views.create_issue, name='create_issue'),
    path('create_volume/', views.create_volume, name='create_volume'),
    path('manage_volumes/', views.manage_volumes, name='manage_volumes'),
    path('manage_volumes/issue/<int:issue_id>/', views.manage_issue, name='manage_issue'),
    path('issues/<int:issue_id>/', views.issue_detail, name='issue_detail'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('search/', views.search, name='search'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),

    # Static Pages
    path('about/', TemplateView.as_view(template_name='journal/about.html'), name='about'),
    path('about/aim-scope/', TemplateView.as_view(template_name='journal/aim_scope.html'), name='aim_scope'),
    path('about/editorial-team/', TemplateView.as_view(template_name='journal/editorial_team.html'), name='editorial_team'),
    path('about/publication-schedule/', TemplateView.as_view(template_name='journal/publication_schedule.html'), name='publication_schedule'),
    path('about/publication-fees/', TemplateView.as_view(template_name='journal/publication_fees.html'), name='publication_fees'),
    path('about/contact/', TemplateView.as_view(template_name='journal/contact.html'), name='contact'),
    path('publications/', TemplateView.as_view(template_name='journal/publications.html'), name='publications'),
    path('publications/current/', views.current_issue, name='current_issue'),
    path('publications/archives/', views.archives, name='archives'),
    path('indexing/', TemplateView.as_view(template_name='journal/indexing.html'), name='indexing'),

    path('metrics/', TemplateView.as_view(template_name='journal/metrics.html'), name='metrics'),
    path('guidelines/', TemplateView.as_view(template_name='journal/guidelines.html'), name='guidelines'),
    path('guidelines/author/', TemplateView.as_view(template_name='journal/author_guidelines.html'), name='author_guidelines'),
    path('guidelines/reviewer/', TemplateView.as_view(template_name='journal/reviewer_guidelines.html'), name='reviewer_guidelines'),
    path('policies/ethics/', TemplateView.as_view(template_name='journal/ethics_malpractice.html'), name='ethics_malpractice'),
    path('policies/open-access/', TemplateView.as_view(template_name='journal/open_access_policy.html'), name='open_access_policy'),
    path('policies/editorial/', TemplateView.as_view(template_name='journal/editorial_policy.html'), name='editorial_policy'),
    path('policies/peer-review/', TemplateView.as_view(template_name='journal/peer_review_policy.html'), name='peer_review_policy'),
    path('policies/archiving/', TemplateView.as_view(template_name='journal/archiving_policy.html'), name='archiving_policy'),
    path('policies/subscription/', TemplateView.as_view(template_name='journal/subscription_advertising.html'), name='subscription_advertising'),
    path('policies/plagiarism/', TemplateView.as_view(template_name='journal/plagiarism_policy.html'), name='plagiarism_policy'),
    path('policies/', TemplateView.as_view(template_name='journal/policies.html'), name='policies'),
    path('announcements/', TemplateView.as_view(template_name='journal/announcements.html'), name='announcements'),
    path('jhst-journals/', TemplateView.as_view(template_name='journal/jhst_journals.html'), name='jhst_journals'),
]
