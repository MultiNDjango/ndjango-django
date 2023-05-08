from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from django.contrib.auth import authenticate
import json

# 회원가입 폼
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='이메일은 필수 입력값 입니다.')

    class Meta:
        model = CustomUser
        fields = ["email", "nickname", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = CustomUser.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"{email}은 이미 존재하는 이메일입니다.")
 
    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        try:
            account = CustomUser.objects.get(nickname=nickname)
        except Exception as e:
            return nickname
        raise forms.ValidationError(f"{nickname}은 이미 존재하는 닉네임입니다.")



# 로그인 폼
class AccountAuthForm(forms.ModelForm):
    email = forms.EmailField(label='email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
 
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
 
    def clean(self):
        cleaned_data = super(AccountAuthForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password') 
        user = authenticate(email=email, password=password)       

        return cleaned_data


# AGE_CHOICES = [(i, str(i)) for i in range(1, 101)]


class CustomUserChangeForm(UserChangeForm):
    AGE_CHOICES = [(i, str(i)) for i in range(1, 101)]

    age = forms.ChoiceField(choices=AGE_CHOICES, label="나이")

    allergy = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="알러지",
        choices=(
            ('nuts', '땅콩'),
            ('seafood', '해산물'),
            ('eggs', '달걀'),
            ('bean', '콩'),
            ('wheat', '밀'),
            ('milk', '우유'),
            ('mackerel', '고등어'),
            ('crab', '게'),
            ('shirimp', '새우'),
            ('pork', '돼지고기'),
            ('peach', '복숭아'),
            ('tomato', '토마토'),
            ('walnut', '호두'),
            ('chicken', '닭고기'),
            ('pork', '쇠고기'),
            ('squid', '오징어'),
            ('oyster', '굴'),
        ),
    )

    password = None

    class Meta:
        model = CustomUser
        fields = ("email", "nickname", "age", "allergy")
        labels = {
            "email" : "이메일",
            "nickname" : "닉네임",
        }

    def clean_age(self):
        age = int(self.cleaned_data.get('age'))
        if age <= 0:
            raise forms.ValidationError("나이는 0보다 작을 수 없습니다.")
        return age

    def save(self, commit=True):
        user = super().save(commit=False)
        allergy = self.cleaned_data.get('allergy')
        allergy = {'allergy': allergy}
        user.allergy = allergy
        # user.allergy = json.dumps(allergy)
        if commit:
            user.save()
        return user

