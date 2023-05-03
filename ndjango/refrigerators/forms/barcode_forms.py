from django import forms

class BarcodeForm(forms.Form):
    image = forms.ImageField()