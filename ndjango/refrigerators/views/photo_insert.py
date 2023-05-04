from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.http import HttpResponse
from refrigerators.forms.base_forms import GrocForm
from refrigerators.forms.photo_forms import PhotoForm
from refrigerators.models.base_models import Grocery
import requests

'''
음식 사진 입력 모듈
'''

# 분석할 사진 업로드
def photo_upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # Pass image to the predict function
            image = form.cleaned_data['image']
            response = requests.post('http://127.0.0.1:5000/predict', files={'image': image})
            prediction = response.json()
            predicted_name = convert_to_grocery_data(prediction)['name']
            request.session['predicted_name'] = predicted_name  # Store the predicted name in the session
            return redirect('refrigerators:register_manual')
    else:
        form = PhotoForm()
    return render(request, 'refrigerators/photo_upload.html', {'form': form})

# 사진 분석
def process_image(image):
    # Flask 앱으로 접속해 분석 진행
    url = 'http://localhost:5000/predict'
    files = {'image': image}
    response = requests.post(url, files=files)
    print(response.json())
    prediction = response.json()
    return prediction

def convert_to_grocery_data(prediction):
    # Convert the prediction to a list of dictionaries
    results = prediction['results']
    
    # Initialize the Grocery model data dictionary
    grocery_data = {'name': '', 'category': '', 'expiration_date': None}
    
    # Set the name and category fields based on the top predicted object
    if results:
        top_result = results[0]
        grocery_data['name'] = top_result['name']
        # grocery_data['category'] = top_result['category']
    
    return grocery_data

