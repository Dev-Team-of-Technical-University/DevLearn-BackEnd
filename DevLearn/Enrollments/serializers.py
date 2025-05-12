from rest_framework import serializers

from Accounts.models import User
from Courses.models import Course
from .models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at', 'is_paid']
