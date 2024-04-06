# forms.py
from django import forms
from .models import UserRegistration

class SignupForm(forms.ModelForm):
    agree_to_terms = forms.BooleanField(required=True, error_messages={'required': 'You must agree to the terms.'})
    class Meta:
        model = UserRegistration
        fields = ['name', 'username', 'email', 'password', 'agree_to_terms']
        widgets = {
            'password': forms.PasswordInput(),
        }


