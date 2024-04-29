# news/forms.py
# forms.py
from django import forms
from .models import registeredUsers, Company
from django.forms import ModelChoiceField
class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = registeredUsers
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'email', 'company']
        company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.Select(attrs={'class': 'dropdown'}))
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if registeredUsers.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())

# forms.py
from django import forms
from .models import Source

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['source_name', 'source_url']

# forms.py
from django import forms
from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'published_date', 'body_text', 'url', 'source', 'company', 'client']

    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        # You can customize form fields here if needed
