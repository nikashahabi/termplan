from django import forms

from src.models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'department', 'password']
        widgets = {
            'password': forms.PasswordInput(),
            'department': forms.Select()
        }
