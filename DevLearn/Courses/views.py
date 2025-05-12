# courses/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from Accounts.models import User
from .models import Category, Tag, Course, Lesson
from .serializers import CategorySerializer, TagSerializer, CourseSerializer, LessonSerializer
import django_filters


class CourseFilter(django_filters.FilterSet):
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte',
                                            label='Price Greater than or Equal to')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Price Less than or Equal to')
    is_published = django_filters.BooleanFilter(field_name='is_published', label='Published Status')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label="Category")
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), to_field_name='name', label="Tags")
    teacher = django_filters.ModelChoiceFilter(queryset=User.objects.filter(role='teacher'), field_name='teacher',
                                               label="Teacher")

    class Meta:
        model = Course
        fields = ['price_gte', 'price_lte', 'is_published', 'category', 'tags', 'teacher']


class LessonFilter(django_filters.FilterSet):
    duration_gte = django_filters.NumberFilter(field_name='duration', lookup_expr='gte',
                                               label='Duration Greater than or Equal to')
    duration_lte = django_filters.NumberFilter(field_name='duration', lookup_expr='lte',
                                               label='Duration Less than or Equal to')

    class Meta:
        model = Lesson
        fields = ['duration_gte', 'duration_lte']


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CourseFilter
    search_fields = ['title', 'description', 'category__title', 'tags__name', 'teacher__full_name']

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('order')
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # فقط کاربران لاگین شده می‌توانند دسته‌بندی‌ها را ویرایش کنند
    search_fields = ['title']

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # مشابه دسته‌بندی‌ها
    search_fields = ['name']