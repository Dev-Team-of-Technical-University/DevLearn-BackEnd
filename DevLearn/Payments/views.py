from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework import filters


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    # فیلتر کردن و جستجو
    search_fields = ['user__fullname', 'course__title', 'ref_id']
    filterset_fields = ['is_successful', 'course', 'user']

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user
        if user.role != 'admin':
            queryset = queryset.filter(user=user)
        return queryset
