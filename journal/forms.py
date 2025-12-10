from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Manuscript, Review

class ResearcherRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'affiliation']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_researcher = True
        if commit:
            user.save()
        return user

class ManuscriptForm(forms.ModelForm):
    class Meta:
        model = Manuscript
        fields = ['title', 'abstract', 'file', 'keywords']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comments', 'recommendation']
