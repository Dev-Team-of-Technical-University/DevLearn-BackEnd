from rest_framework import viewsets, permissions, filters
from .models import Comment
from .serializers import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
import django_filters


class CommentFilter(django_filters.FilterSet):
    rating_gte = django_filters.NumberFilter(field_name='rating', lookup_expr='gte', label="امتیاز بیشتر یا مساوی")

    class Meta:
        model = Comment
        fields = ['course', 'user', 'rating_gte']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = CommentFilter
    search_fields = ['content', 'course__title', 'user__username']  # جستجو در متن کامنت، عنوان دوره، یا شماره کاربر

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
