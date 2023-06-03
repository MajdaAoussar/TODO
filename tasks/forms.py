from django import forms
from .models import Task
from django.utils.translation import gettext_lazy as _

class AddNewTask(forms.ModelForm):
    class Meta:
        model= Task
        fields= ['description','user']
        labels= {
            'description': _('')
        }
        widgets= {
            'description': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter description'}),
            'user': forms.HiddenInput()
        }

    