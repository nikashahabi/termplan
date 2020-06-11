from django import forms
from src.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, id='username')
    choices = (('ریاضی', 'ریاضی'), ('علوم کامپیوتر', 'علوم کامپیوتر'),)
    field = forms.ChoiceField(choices=choices)

    class Meta:
        model = User
        fields = ('username', 'department', 'password',)
        widgets = {
            'password': forms.PasswordInput()
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'department', 'password']
        widgets = {
            'password': forms.PasswordInput(),
            'department': forms.Select()
        }
