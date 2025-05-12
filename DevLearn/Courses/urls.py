# courses/urls.py
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TagViewSet, CourseViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = router.urls
