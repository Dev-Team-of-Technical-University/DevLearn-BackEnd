from django.utils import timezone

from django import forms
from Accounts.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 'full_name', 'role', 'email']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("این شماره قبلاً ثبت شده است.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
    username = forms.CharField(label="نام کاربری")
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)


class ForgetPasswordRequestForm(forms.Form):
    email = forms.EmailField(label="ایمیل")

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("کاربری با این ایمیل وجود ندارد.")
        return email


class ForgetPasswordConfirmForm(forms.Form):
    email = forms.EmailField(label="ایمیل")
    code = forms.CharField(max_length=6, label="کد تأیید")
    new_password = forms.CharField(label="رمز عبور جدید", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        code = cleaned_data.get("code")

        try:
            user = User.objects.get(email=email, phone_verify_code=code)
        except User.DoesNotExist:
            raise forms.ValidationError("کد تأیید یا ایمیل اشتباه است.")

        if user.phone_verify_code_created and (timezone.now() - user.phone_verify_code_created).total_seconds() > 600:
            raise forms.ValidationError("کد منقضی شده است.")

        cleaned_data['user'] = user
        return cleaned_data

    def save(self):
        user = self.cleaned_data['user']
        new_password = self.cleaned_data['new_password']
        user.set_password(new_password)
        user.phone_verify_code = None
        user.phone_verify_code_created = None
        user.save()
        return user