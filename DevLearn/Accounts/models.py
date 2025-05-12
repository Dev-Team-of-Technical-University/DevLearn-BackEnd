from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # پسورد را هش می‌کند
        user.date_joined = timezone.now()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    phone_regex = RegexValidator(regex=r'^09\d{9}$', message="Phone must be entered in the format: 09xxxxxxxxx")
    phone = models.CharField(validators=[phone_regex], max_length=11)
    username = models.CharField(max_length=100, unique=True, verbose_name="username")
    password = models.CharField(max_length=100, verbose_name="password")

    full_name = models.CharField(max_length=100, blank=True)

    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    specialty = models.CharField(max_length=255, blank=True)  # برای مدرس‌ها

    date_joined = models.DateTimeField(default=timezone.now)
    phone_verified = models.BooleanField(default=False)
    phone_verify_code = models.CharField(max_length=6, null=True, blank=True)
    phone_verify_code_created = models.DateTimeField(null=True, blank=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.full_name or 'No Name'} - {self.phone}"
