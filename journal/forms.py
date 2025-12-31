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
                'class': 'w-full px-4 py-3 border border-slate-300 rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary text-sm dark:bg-card-dark dark:border-slate-600 dark:text-white transition-all duration-200'
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
            'abstract': forms.Textarea(attrs={'rows': 12}),
            'affiliations': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 border border-slate-300 rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary text-sm dark:bg-card-dark dark:border-slate-600 dark:text-white transition-all duration-200'
            })

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comments', 'recommendation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 border border-slate-300 rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary text-sm dark:bg-card-dark dark:border-slate-600 dark:text-white transition-all duration-200'
            })

class VolumeForm(forms.ModelForm):
    class Meta:
        model = Volume
        fields = ['number', 'year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 border border-slate-300 rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary text-sm dark:bg-card-dark dark:border-slate-600 dark:text-white transition-all duration-200'
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
                'class': 'w-full px-4 py-3 border border-slate-300 rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary text-sm dark:bg-card-dark dark:border-slate-600 dark:text-white transition-all duration-200'
            })

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary text-sm dark:bg-card-dark dark:border-slate-600 dark:text-white transition-all duration-200'
            })
