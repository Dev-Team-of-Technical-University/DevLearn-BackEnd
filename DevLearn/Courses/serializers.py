from rest_framework import serializers
from .models import Category, Tag, Course, Lesson

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'video', 'order', 'duration']



class CourseSerializer(serializers.ModelSerializer):
    teacher_full_name = serializers.CharField(source='teacher.full_name', read_only=True)
    category_title = serializers.CharField(source='category.title', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'teacher', 'teacher_full_name', 'title', 'description', 'category', 'category_title', 'tags', 'thumbnail', 'price', 'is_published', 'created_at']
        read_only_fields = ['id', 'created_at']
