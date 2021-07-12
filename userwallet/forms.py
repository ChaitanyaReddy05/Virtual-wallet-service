from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import wallet


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']



class RedeemPointsForm(forms.Form):
    gamepoints =  forms.IntegerField(label='Points (minimum 10)', min_value=10)

