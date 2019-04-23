from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'display_name',
            'avatar'
        ]

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        email = data.get('email', None)
        if email == "":
            email = None
        display_name = data.get('display_name', None)
        if email is None and display_name is None:
            raise forms.ValidationError('Email or Name is required')
        return super().clean(*args, **kwargs)
