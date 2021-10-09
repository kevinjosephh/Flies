from django.db.models import fields
from django.forms import ModelForm
from .models import *


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'