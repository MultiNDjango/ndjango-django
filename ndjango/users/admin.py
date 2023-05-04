
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegistrationForm, CustomUserChangeForm
from .models import CustomUser
from .managers import CustomUserManager


class CustomUserAdmin(UserAdmin):
    # 관리자 화면에 보여질 칼럼
    add_form = RegistrationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "nickname", "age", "diet", "allergy")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email", "nickname")
    ordering = ("email", "nickname")


admin.site.register(CustomUser, CustomUserAdmin)