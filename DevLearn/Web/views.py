import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from Accounts.models import User
from Courses.models import Course
from Web.forms import LoginForm, RegisterForm, ForgetPasswordRequestForm, ForgetPasswordConfirmForm


@login_required
def home_page(request):
    courses = Course.objects.all()
    return render(request, "home/index.html", {"courses": courses})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ثبت‌نام با موفقیت انجام شد.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home_page')  # یا هر صفحه‌ای بعد از لاگین
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید.")
    return redirect('login')


def forget_password_request_view(request):
    if request.method == 'POST':
        form = ForgetPasswordRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            code = str(random.randint(100000, 999999))
            user.phone_verify_code = code
            user.phone_verify_code_created = timezone.now()
            user.save()

            # ارسال ایمیل
            send_mail(
                subject="بازیابی رمز عبور",
                message=f"کد تأیید شما: {code}",
                from_email=None,
                recipient_list=[email],
            )
            messages.success(request, "کد تأیید به ایمیل شما ارسال شد.")
            return redirect('forget-password-confirm')
    else:
        form = ForgetPasswordRequestForm()
    return render(request, 'accounts/forget_password_request.html', {'form': form})


def forget_password_confirm_view(request):
    if request.method == 'POST':
        form = ForgetPasswordConfirmForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
            return redirect('login')
    else:
        form = ForgetPasswordConfirmForm()
    return render(request, 'accounts/forget_password_confirm.html', {'form': form})


def course_list(request):
    pass


def about_us(request):
    return render(request, "home/about_us.html")


def contact_us(request):
    return render(request, "home/contact_us.html")
