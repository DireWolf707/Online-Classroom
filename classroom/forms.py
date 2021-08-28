from django import forms
from .models import Classroom
#from django.core.exceptions import ValidationError
#from django.core import validators


class CreateClassForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ('name',)


class JoinClassForm(forms.Form):
    code = forms.CharField(max_length=10, min_length=10)
