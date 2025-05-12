from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
import random
from django.utils import timezone
from django.core.mail import send_mail


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 'full_name', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("نام کاربری یا رمز عبور اشتباه است.")
        if not user.is_active:
            raise serializers.ValidationError("حساب کاربری غیرفعال است.")
        data['user'] = user
        return data



class ForgetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("کاربری با این ایمیل وجود ندارد.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
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
            fail_silently=False,
        )
        return user


class ForgetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        code = data.get("code")
        user_qs = User.objects.filter(email=email, phone_verify_code=code)

        if not user_qs.exists():
            raise serializers.ValidationError("کد تأیید یا ایمیل اشتباه است.")

        user = user_qs.first()

        if user.phone_verify_code_created and timezone.now() - user.phone_verify_code_created > timezone.timedelta(
                minutes=10):
            raise serializers.ValidationError("کد منقضی شده است.")

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.phone_verify_code = None
        user.phone_verify_code_created = None
        user.save()
        return user
