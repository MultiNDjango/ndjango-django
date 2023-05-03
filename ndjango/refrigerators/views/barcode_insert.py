import cv2
from django.shortcuts import render, get_object_or_404
from pyzbar import pyzbar
from refrigerators.models import BarcodeInfo
import numpy as np

from refrigerators.forms.barcode_forms import BarcodeForm


def search_barcode(request):
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        photo = request.FILES.get('photo')
        if barcode:
            barcode_info = BarcodeInfo.objects.filter(barcode=barcode).first()
            if barcode_info:
                context = {'barcode_info': barcode_info, 'photo': photo}
                return render(request, 'refrigerators/barcode_info.html', context)
        elif photo:
            barcode_data = barcode_img_reader(photo)
            barcode_info = BarcodeInfo.objects.filter(barcode=barcode_data).first()
            if barcode_info:
                context = {'barcode_info': barcode_info, 'photo': photo}
                return render(request, 'refrigerators/barcode_info.html', context)
    return render(request, 'refrigerators/search_barcode.html')


def barcode_info(request, barcode):
    barcode_info = get_object_or_404(BarcodeInfo, barcode=barcode)
    context = {'barcode_info': barcode_info}
    return render(request, 'refrigerators/barcode_info.html', context)


def upload(request):
    if request.method == 'POST':
        form = BarcodeForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data['photo']
            context = {'uploaded_file_url': photo.url}
            barcode_data = barcode_img_reader(photo)
            barcode_info = BarcodeInfo.objects.filter(barcode=barcode_data).first()
            if barcode_info:
                context = {'barcode_info': barcode_info, 'photo': photo}
                return render(request, 'refrigerators/barcode_info.html', context)
    else:
        form = BarcodeForm()
    return render(request, 'refrigerators/search_barcode.html', {'form': form})


def barcode_img_reader(photo):
    used_codes = []
    img = cv2.imdecode(np.frombuffer(photo.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)

    if len(barcodes) == 0:
        print("바코드를 찾을 수 없습니다.")
        exit()

    for barcode in barcodes:
        barcode_data = "a"+barcode.data.decode("utf-8")
        used_codes.append(barcode_data)
    return used_codes[0]