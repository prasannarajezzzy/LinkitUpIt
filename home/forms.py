from django import forms
from django.contrib.auth.models import User
from home.models import Job, JobCategory, JobStatus

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        help_texts = {
            'username': None
        }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class JobEntryForm(forms.ModelForm):
    company = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    category = forms.ModelChoiceField(queryset=JobCategory.objects.all())
    status = forms.ModelChoiceField(queryset=JobStatus.objects.all())
    pdf_file = forms.FileField()
    class Meta():
        model = Job
        fields = ('company','description', 'category', 'status')


# ---------------------- Prasanna code

class PdfUploadForm(forms.Form):
    pdf_file = forms.FileField()

