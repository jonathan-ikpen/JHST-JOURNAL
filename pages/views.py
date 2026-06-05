from django.shortcuts import render
from journal.models import Issue
from .models import (
    HomePage, OrganogramItem, AboutPage, AimScopePage, ContactPage,
    PublicationFeesPage, EditorialTeamPage, TeamMember, IndexingPage,
    IndexingEntry, PoliciesPage, AuthorGuidelinesPage, EthicsMalpracticePage,
    OpenAccessPolicyPage, PeerReviewPolicyPage, ArchivingPolicyPage,
    PlagiarismPolicyPage, SubscriptionAdvertisingPage, EditorialPolicyPage,
    PublicationSchedulePage, GuidelinesPage, ReviewerGuidelinesPage,
    MetricsPage, JhstJournalsPage, PtiJournal, PublicationsPage,
)


def home(request):
    page = HomePage.objects.get(pk=1)
    organogram = OrganogramItem.objects.all()
    latest_issues = Issue.objects.all().order_by('-publication_date')[:5]
    return render(request, 'journal/index.html', {
        'page': page,
        'organogram': organogram,
        'latest_issues': latest_issues,
    })


def about(request):
    page = AboutPage.objects.get(pk=1)
    return render(request, 'journal/about.html', {'page': page})


def aim_scope(request):
    page = AimScopePage.objects.get(pk=1)
    return render(request, 'journal/aim_scope.html', {'page': page})


def contact(request):
    page = ContactPage.objects.get(pk=1)
    return render(request, 'journal/contact.html', {'page': page})


def publication_fees(request):
    page = PublicationFeesPage.objects.get(pk=1)
    return render(request, 'journal/publication_fees.html', {'page': page})


def editorial_team(request):
    page = EditorialTeamPage.objects.get(pk=1)
    members = TeamMember.objects.all()
    editor_in_chief = members.filter(role_type='editor_in_chief').first()
    managing_directors = members.filter(role_type='managing_director')
    editorial_assistants = members.filter(role_type='editorial_assistant')
    section_editors = members.filter(role_type='section_editor')
    editorial_board = members.filter(role_type='editorial_board')
    return render(request, 'journal/editorial_team.html', {
        'page': page,
        'editor_in_chief': editor_in_chief,
        'managing_directors': managing_directors,
        'editorial_assistants': editorial_assistants,
        'section_editors': section_editors,
        'editorial_board': editorial_board,
    })


def indexing(request):
    page = IndexingPage.objects.get(pk=1)
    entries = IndexingEntry.objects.all()
    return render(request, 'journal/indexing.html', {'page': page, 'entries': entries})


def policies(request):
    page = PoliciesPage.objects.get(pk=1)
    return render(request, 'journal/policies.html', {'page': page})


def author_guidelines(request):
    page = AuthorGuidelinesPage.objects.get(pk=1)
    return render(request, 'journal/author_guidelines.html', {'page': page})


def ethics_malpractice(request):
    page = EthicsMalpracticePage.objects.get(pk=1)
    return render(request, 'journal/ethics_malpractice.html', {'page': page})


def open_access_policy(request):
    page = OpenAccessPolicyPage.objects.get(pk=1)
    return render(request, 'journal/open_access_policy.html', {'page': page})


def peer_review_policy(request):
    page = PeerReviewPolicyPage.objects.get(pk=1)
    return render(request, 'journal/peer_review_policy.html', {'page': page})


def archiving_policy(request):
    page = ArchivingPolicyPage.objects.get(pk=1)
    return render(request, 'journal/archiving_policy.html', {'page': page})


def plagiarism_policy(request):
    page = PlagiarismPolicyPage.objects.get(pk=1)
    return render(request, 'journal/plagiarism_policy.html', {'page': page})


def subscription_advertising(request):
    page = SubscriptionAdvertisingPage.objects.get(pk=1)
    return render(request, 'journal/subscription_advertising.html', {'page': page})


def editorial_policy(request):
    page = EditorialPolicyPage.objects.get(pk=1)
    return render(request, 'journal/editorial_policy.html', {'page': page})


def publication_schedule(request):
    page = PublicationSchedulePage.objects.get(pk=1)
    return render(request, 'journal/publication_schedule.html', {'page': page})


def guidelines(request):
    page = GuidelinesPage.objects.get(pk=1)
    return render(request, 'journal/guidelines.html', {'page': page})


def reviewer_guidelines(request):
    page = ReviewerGuidelinesPage.objects.get(pk=1)
    return render(request, 'journal/reviewer_guidelines.html', {'page': page})


def metrics(request):
    page = MetricsPage.objects.get(pk=1)
    return render(request, 'journal/metrics.html', {'page': page})


def jhst_journals(request):
    page = JhstJournalsPage.objects.get(pk=1)
    journals = PtiJournal.objects.all()
    return render(request, 'journal/jhst_journals.html', {'page': page, 'journals': journals})


def publications(request):
    page = PublicationsPage.objects.get(pk=1)
    return render(request, 'journal/publications.html', {'page': page})
