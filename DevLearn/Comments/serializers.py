from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_phone', 'course', 'course_title', 'content', 'rating', 'created_at']
        read_only_fields = ['id', 'created_at']
