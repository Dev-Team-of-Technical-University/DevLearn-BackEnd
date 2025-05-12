from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Enrollment
from .serializers import EnrollmentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    # فیلتر و جستجو
    search_fields = ['user__phone', 'course__title']
    filterset_fields = ['is_paid']

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user
        if user.role != 'admin':
            queryset = queryset.filter(user=user)
        return queryset
