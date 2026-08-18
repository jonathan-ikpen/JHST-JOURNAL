from django.urls import path, reverse_lazy
from . import views, feeds
from .forms import UserLoginForm, CustomPasswordChangeForm
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from pages import views as pages_views

class CustomPasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    success_message = "Your password was successfully updated!"

urlpatterns = [
    path('', pages_views.home, name='index'),
    path('register/', views.register, name='register'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification_email, name='resend_verification'),
    path('login/', auth_views.LoginView.as_view(template_name='journal/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/manuscript/<int:manuscript_id>/', views.dashboard_manuscript_detail, name='dashboard_manuscript_detail'),
    path('dashboard/my-submissions/', views.my_submissions, name='my_submissions'),
    path('dashboard/my-submission/<int:manuscript_id>/', views.my_submission_detail, name='my_submission_detail'),
    path('dashboard/my-submission/<int:manuscript_id>/submit-revision/', views.submit_revision, name='submit_revision'),
    path('dashboard/review-assignment/<int:review_id>/', views.reviewer_manuscript_detail, name='reviewer_manuscript_detail'),
    path('dashboard/assigned-reviews/', views.assigned_reviews, name='assigned_reviews'),
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', CustomPasswordChangeView.as_view(
        template_name='journal/change_password.html', 
        success_url=reverse_lazy('profile'),
        form_class=CustomPasswordChangeForm
    ), name='change_password'),
    path('submit/', views.submit_manuscript, name='submit_manuscript'),
    path('assign_reviewer/<int:manuscript_id>/', views.assign_reviewer, name='assign_reviewer'),
    path('request_re_review/<int:review_id>/', views.request_re_review, name='request_re_review'),
    path('submit_review/<int:review_id>/', views.submit_review, name='submit_review'),
    path('accept_invitation/<int:review_id>/', views.accept_review_invitation, name='accept_invitation'),
    path('decline_invitation/<int:review_id>/', views.decline_review_invitation, name='decline_invitation'),
    path('reviewer_check_revision/<int:review_id>/', views.reviewer_check_revision, name='reviewer_check_revision'),
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

    # Static Pages — backed by pages app models
    path('about/', pages_views.about, name='about'),
    path('about/aim-scope/', pages_views.aim_scope, name='aim_scope'),
    path('about/editorial-team/', pages_views.editorial_team, name='editorial_team'),
    path('about/publication-schedule/', pages_views.publication_schedule, name='publication_schedule'),
    path('about/publication-fees/', pages_views.publication_fees, name='publication_fees'),
    path('about/contact/', pages_views.contact, name='contact'),
    path('publications/', pages_views.publications, name='publications'),
    path('conferences/', pages_views.conferences, name='conferences'),
    path('publications/current/', views.current_issue, name='current_issue'),
    path('publications/archives/', views.archives, name='archives'),
    path('indexing/', pages_views.indexing, name='indexing'),
    path('metrics/', pages_views.metrics, name='metrics'),
    path('guidelines/', pages_views.guidelines, name='guidelines'),
    path('guidelines/author/', pages_views.author_guidelines, name='author_guidelines'),
    path('guidelines/reviewer/', pages_views.reviewer_guidelines, name='reviewer_guidelines'),
    path('policies/ethics/', pages_views.ethics_malpractice, name='ethics_malpractice'),
    path('policies/open-access/', pages_views.open_access_policy, name='open_access_policy'),
    path('policies/editorial/', pages_views.editorial_policy, name='editorial_policy'),
    path('policies/peer-review/', pages_views.peer_review_policy, name='peer_review_policy'),
    path('policies/archiving/', pages_views.archiving_policy, name='archiving_policy'),
    path('policies/subscription/', pages_views.subscription_advertising, name='subscription_advertising'),
    path('policies/plagiarism/', pages_views.plagiarism_policy, name='plagiarism_policy'),
    path('policies/', pages_views.policies, name='policies'),
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/<int:announcement_id>/', views.announcement_detail, name='announcement_detail'),
    path('jhst-journals/', pages_views.jhst_journals, name='jhst_journals'),
    path('rss/', feeds.LatestArticlesFeed(), name='article_feed'),
]
