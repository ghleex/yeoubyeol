from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Waiting


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = '__all__'


class WaitingForm(forms.ModelForm):
    username = forms.CharField(required=True)
    secret_key = forms.CharField(required=False)
    class Meta:
        model = Waiting
        fields = ("username",)


# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = get_user_model()
#         fields = '__all__'

