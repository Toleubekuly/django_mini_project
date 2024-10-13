from django import forms
from django.contrib.auth.models import User
from .models import ProfileF

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileF
        fields = ['bio', 'profile_picture']


class ProfileEditForm(ProfileForm):
    pass
