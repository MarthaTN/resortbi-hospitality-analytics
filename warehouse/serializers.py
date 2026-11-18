from rest_framework import serializers

from .models import TrustedReservation


class TrustedReservationSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = TrustedReservation

        fields = [
            "id",
            "reservation_number",
            "guest_name",
            "country",
            "resort_name",
            "check_in",
            "check_out",
            "booking_status",
            "amount",
            "processed_at",
        ]

        read_only_fields = [
            "id",
            "processed_at",
        ]