from rest_framework import viewsets

from .models import TrustedReservation
from .serializers import TrustedReservationSerializer
from core.permissions import IsAdministratorOrAnalyst



class TrustedReservationViewSet(
    viewsets.ReadOnlyModelViewSet
):

    serializer_class = TrustedReservationSerializer

    permission_classes = [IsAdministratorOrAnalyst]

    def get_queryset(self):

        queryset = TrustedReservation.objects.all().order_by(
            "-processed_at"
        )

        resort_name = self.request.query_params.get(
            "resort_name"
        )

        country = self.request.query_params.get(
            "country"
        )

        booking_status = self.request.query_params.get(
            "booking_status"
        )

        if resort_name:
            queryset = queryset.filter(
                resort_name__icontains=resort_name
            )

        if country:
            queryset = queryset.filter(
                country__icontains=country
            )

        if booking_status:
            queryset = queryset.filter(
                booking_status__iexact=booking_status
            )

        return queryset