from django.shortcuts import render, redirect
from django.http import HttpResponse
from refrigerators.forms.base_forms import GrocForm
from refrigerators.forms.photo_forms import PhotoForm
from refrigerators.models.base_models import Grocery

'''
음식 사진 입력 모듈
'''

# 객체 검출 모델 및 추론 모듈은 별도의 restAPI 서버에 구현 후 api call을 통해 output만 받아서 화면에 디스플레이 하기

def photo_upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # Pass image to AI algorithm for processing
            processed_data = process_image(form.cleaned_data['image'])
            # Convert processed data to Grocery model format
            grocery_data = convert_to_grocery_data(processed_data)
            # Save data to database
            grocery = Grocery(**grocery_data)
            grocery.save()
            return redirect('grocery_list')
    else:
        form = PhotoForm()
    return render(request, 'refrigerators/photo_upload.html', {'form': form})

# ai.py
def process_image(image):
    # Code to process image using AI algorithm
    pass

def convert_to_grocery_data(processed_data):
    # Code to convert processed data into Grocery model format
    pass

def register_photo(request):
    if request.method == 'POST':
        form = GrocForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('grocery_list')
    else:
        form = GrocForm()
    return render(request, 'refrigerators/photo_register.html', {'form': form})
