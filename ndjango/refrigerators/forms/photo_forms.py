# -*- coding: utf-8 -*-
from django import forms
# from refrigerators.models.photo_models import *

class PhotoForm(forms.Form):
    image = forms.ImageField()
    
