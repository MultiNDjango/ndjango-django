from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from refrigerators.forms.base_forms import *
from refrigerators.models import Grocery
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.views.static import serve
from django.contrib import messages
from django.utils import timezone
import os

from refrigerators.views.base_to_icon import set_grocery_location
from refrigerators.views.base_to_icon import remove_grocery_location

'''
수기 입력 및 CRUD 모듈 + 알림 모듈
'''

# index 페이지 view
@login_required(login_url='users:login')
def index(request):
    page = request.GET.get('page', '1')
    grocery_list = Grocery.objects.filter(userid_id=request.user).order_by('exp_date')

    paginator = Paginator(grocery_list, 10)
    page_obj = paginator.get_page(page)

    today = timezone.now().date()
    expiring_groceries = []
    expired_groceries = []
    for grocery in grocery_list:
        days_until_expire = (grocery.exp_date - today).days
        if days_until_expire < 0:
            expired_groceries.append(grocery)
        elif days_until_expire <= 3:
            expiring_groceries.append(grocery)
    if expired_groceries:
        messages.error(request, f"소비기한이 만료된 식재료가 {len(expired_groceries)}개 있어요!", extra_tags='alert-dismissible expired')
    if expiring_groceries:
        messages.warning(request, f"소비기한이 3일 내에 만료되는 식재료가 {len(expiring_groceries)}개 있어요!", extra_tags='alert-dismissible expiring')
    context = {'grocery_list': page_obj}
    return render(request, 'refrigerators/crud_index.html', context)

def insertion_method(request):
    if request.method == 'POST':
        insertion_method = request.POST.get('insertion_method')
        if insertion_method == 'manual':
            return redirect('refrigerators:register_manual')
        elif insertion_method == 'photo':
            return redirect('refrigerators:photo_upload')
        elif insertion_method == 'barcode':
            return redirect('refrigerators:register_barcode')
        else:
            # If an invalid insertion method was selected, render the template with an error message
            error_message = '입력 방법이 제대로 선택되지 않았습니다. 다시 시도해주세요.'
            return render(request, 'refrigerators/insertion_method.html', {'error_message': error_message})
    else:
        # If the request method was not POST, render the template without an error message
        return render(request, 'refrigerators/insertion_method.html')


# 식재료 등록 페이지 view
def register_manual(request):
    if request.method == 'POST':
        form = GrocForm(request.POST, request.FILES)
        if form.is_valid():
            grocery = form.save(commit=False)
            image = request.FILES.get('image')
            grocery.userid_id = request.user.id
            if image:
                fs = FileSystemStorage()
                filename = fs.save(image.name, image.file)
                grocery.image = filename
            else:
                grocery.image = None

            grocery.save()
            request.session.pop('predicted_name', None)  # Remove the predicted name from the session

            # 냉장고에 식재료 위치 배정
            rst_instance = set_grocery_location(grocery.id, request.user.id)
            if not rst_instance:
                print("fridge is full")

            return redirect('refrigerators:index')
        else:
            error_message = '정보가 제대로 입력되지 않았습니다. 다시 입력해주세요.'
            return render(request, 'refrigerators/crud_register.html', {'error_message': error_message})
    else:
        predicted_name = request.session.pop('predicted_name', None)  # Get the predicted name from the session and remove it
        initial_data = {'name': predicted_name} if predicted_name else {}
        form = GrocForm(initial=initial_data)
        return render(request, 'refrigerators/crud_register.html', {'form': form})

def register_picture(request):
    pass

def register_barcode(request):
    pass

# 식재료 상세 페이지 view
def view(request, pk):
    grocery_list = get_object_or_404(Grocery, id=pk)
    context = {'grocery_list': grocery_list}
    return render(request, 'refrigerators/crud_view.html', context)

# 식재료 정보 수정 페이지 view
def edit(request, pk):
    post = get_object_or_404(Grocery, id=pk)
    if request.method == 'POST':
        form = GrocForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            grocery = form.save(commit=False)

            fs = FileSystemStorage()
            if request.POST.get('image-clear'):  # check if image field was cleared
                # delete the old image file if it exists
                if post.image:
                    fs.delete(post.image.name)
                grocery.image = None
            else:
                image = request.FILES.get('image')
                if image: # 새로운 이미지가 업로드 되면
                    # delete old image
                    fs.delete(post.image.name)
                    grocery.image = None
                    # save new image
                    filename = fs.save(image.name, image.file)
                    grocery.image = filename
                else:
                    # keep the old image
                    grocery.image = post.image
            grocery.save()
            if grocery.qty == 0:
                messages.warning(request, 'The quantity of this grocery is now zero.')
            return redirect('refrigerators:index')
    else:
        form = GrocForm(instance=post)
    context = {'form': form}
    return render(request, 'refrigerators/crud_edit.html', context)

# 식재료 삭제 view
def delete(request, pk):
    grocery = get_object_or_404(Grocery, id=pk)
    grocery.delete()

    # 냉장고에 식재료 위치 삭제
    rst_instance = remove_grocery_location(pk, request.user.id)
    if not rst_instance:
        print("the deleted grocery doesn't have location")

    return redirect('refrigerators:index')

# 식재료 사진 view
def serve_grocery_image(request, pk):
    grocery = get_object_or_404(Grocery, pk=pk)
    if not grocery.image:
        raise Http404("Image not found")
    # construct the path to the image file
    path = os.path.join(settings.MEDIA_ROOT, str(grocery.image.name))
    # serve the image
    return serve(request, path, document_root=settings.MEDIA_ROOT)

def expiring_groceries(request):
    today = timezone.now().date()
    expiring_groceries = Grocery.objects.filter(exp_date__lte=today + timezone.timedelta(days=3))
    context = {'expiring_groceries': expiring_groceries}
    return render(request, 'refrigerators/expiring_groceries.html', context)