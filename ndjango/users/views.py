from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from .models import CustomUser
from django.http import HttpResponse
from .forms import RegistrationForm, CustomUserChangeForm, AccountAuthForm

# Create your views here.

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        
        # 실제 DB에 있는 회원이라면 로그인 진행
        if user is not None:
            login(request, user)
            return redirect('users:login')
        else:
            error_message="이메일 또는 비밀번호를 정확히 입력하세요."
            context = {'error_message': error_message}
            return render(request, "users/login.html", context)
    
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def signup_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            email_errors = form['email'].errors
            nickname_errors = form['nickname'].errors
            password_errors = form['password1'].errors
            password2_errors = form['password2'].errors
    else:
        form = RegistrationForm()
    return render(request, "users/signup.html", {'form': form})

@login_required(login_url='users:login')
def update_view(request):

    if request.method == "POST":

        editForm = CustomUserChangeForm(request.POST, instance=request.user)

        if editForm.is_valid():
            editForm.save()
            return redirect('/users/login')
    else:
        user = request.user
        # print(user.allergy['allergy'])
        if not user.allergy:
            user.allergy = []
        else:
            user.allergy = user.allergy['allergy']
        editForm = CustomUserChangeForm(instance=request.user)


    return render(request, "users/update.html", {'editForm': editForm})
    

