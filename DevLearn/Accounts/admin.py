from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from Accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'full_name', 'phone', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'phone_verified', 'date_joined')
    search_fields = ('username', 'full_name', 'phone', 'email')
    ordering = ('-date_joined',)

    fieldsets = (
        (_('اطلاعات حساب'), {
            'fields': ('username', 'password')
        }),
        (_('اطلاعات شخصی'), {
            'fields': ('full_name', 'email', 'phone', 'role', 'profile_image', 'bio', 'specialty')
        }),
        (_('وضعیت'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'phone_verified')
        }),
        (_('تأیید شماره تماس'), {
            'fields': ('phone_verify_code', 'phone_verify_code_created')
        }),
        (_('مجوزها'), {
            'fields': ('groups', 'user_permissions')
        }),
        (_('تاریخ‌ها'), {
            'fields': ('date_joined',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'phone', 'role', 'is_active', 'is_staff'),
        }),
    )

    readonly_fields = ('date_joined', 'phone_verify_code_created')
