from django import forms
from django.forms import widgets
from refrigerators.models import *

class DateInput(forms.DateInput):
        input_type = 'date'

class GrocForm(forms.ModelForm):
    class Meta:
        model = Grocery
        fields = ['name', 'category', 'qty', 'in_date', 'exp_date', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'qty': forms.NumberInput(attrs={'class': 'form-control'}),
            'in_date': DateInput(attrs={'class': 'form-control'}),
            'exp_date': DateInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
