from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Manuscript, Review, Volume, Issue

class ResearcherRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'affiliation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary sm:text-sm'
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_researcher = True
        if commit:
            user.save()
        return user

class ManuscriptForm(forms.ModelForm):
    class Meta:
        model = Manuscript
        fields = ['title', 'abstract', 'file', 'keywords', 'co_authors', 'affiliations']
        widgets = {
            'abstract': forms.Textarea(attrs={'rows': 4}),
            'affiliations': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary sm:text-sm'
            })

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comments', 'recommendation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary sm:text-sm'
            })

class VolumeForm(forms.ModelForm):
    class Meta:
        model = Volume
        fields = ['number', 'year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary sm:text-sm'
            })

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['volume', 'number', 'publication_date']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary sm:text-sm'
            })

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary sm:text-sm'
            })
