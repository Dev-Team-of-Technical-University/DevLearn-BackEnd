# courses/views.py
from urllib.parse import urlparse
import requests
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
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
        fields = ['price_gte','price_lte', 'is_published', 'category', 'tags', 'teacher']


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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # استخراج مسیر از video_url (مثلاً "/videos/myvideo.mp4")
        remote_path = self.extract_remote_path(instance.video_url)
        fastapi_url = "http://localhost:8000/delete"

        # درخواست حذف از FastAPI
        try:
            response = requests.delete(fastapi_url, json={"remote_path": remote_path})
            if response.status_code not in [200, 404]:
                return Response({"error": "Failed to delete video from Nextcloud."}, status=500)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        # حذف رکورد از دیتابیس
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def extract_remote_path(self, video_url):
        """
        Example:
        input: http://192.168.1.33:8080/remote.php/dav/files/Meysam08/videos/myvideo.mp4
        output: /videos/myvideo.mp4
        """
        if not video_url:
            return ""
        parsed = urlparse(video_url)
        path = parsed.path
        # حذف بخش ثابت مسیر nextcloud تا به مسیر relative برسیم
        parts = path.split("/files/Meysam08/")
        return f"/{parts[1]}" if len(parts) > 1 else ""


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]  # فقط کاربران لاگین شده می‌توانند دسته‌بندی‌ها را ویرایش کنند
    search_fields = ['title']


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # مشابه دسته‌بندی‌ها
    search_fields = ['name']
