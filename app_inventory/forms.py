from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password']


class addproduct(ModelForm):
    class Meta:
        model =Product
        fields = '__all__'

class addu_type(ModelForm):
    class Meta:
        model=u_type
        fields='__all__'
