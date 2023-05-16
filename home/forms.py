from django import forms
from django.contrib.auth.models import User
from home.models import Job, JobCategory, JobStatus
from .api import resume_parse, getResponse, get_keywords,suggest_keywords,calculate_matching_score

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password'}))
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
    category = forms.ModelChoiceField(queryset=JobCategory.objects.all())
    status = forms.ModelChoiceField(queryset=JobStatus.objects.all())
    job_description = forms.CharField(widget=forms.Textarea)
    resume_text = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    class Meta:
        model = Job
        fields = ('company', 'category', 'status', 'job_description', 'resume_text')

    def save(self, commit=True, *args, **kwargs):
        prompt = "Write a cover letter based on Resume and job desccription 150 words strictly"
        instance = super().save(commit=False, *args, **kwargs)
        input_text = prompt + " Job Description :" + \
                instance.job_description + "Resume : " + instance.resume_text + " company name :" +instance.company
 
        instance.cover_letter = getResponse(input_text)
        instance.matching_score = calculate_matching_score(instance.job_description, instance.resume_text )
        instance.suggested_keywords = suggest_keywords(instance.job_description, instance.resume_text )

        # Assign the currently logged-in user as the job's user
        instance.user = self.request.user  # Assumes the view has request attribute

        if commit:
            instance.save()

        return instance

# ---------------------- Prasanna code

class PdfUploadForm(forms.Form):
    pdf_file = forms.FileField()
