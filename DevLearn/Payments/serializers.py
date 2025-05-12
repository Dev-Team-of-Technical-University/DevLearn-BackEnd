from rest_framework import serializers
from .models import Payment
from Courses.models import Course
from Accounts.models import User


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Payment
        fields = ['id', 'user', 'course', 'amount', 'is_successful', 'ref_id', 'created_at']
        read_only_fields = ['created_at']
