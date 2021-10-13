from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','members']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email',]