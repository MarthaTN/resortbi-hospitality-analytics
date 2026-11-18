from rest_framework import serializers

from .models import StagedReservation


class StagedReservationSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = StagedReservation

        fields = [
            "id",
            "source_system",
            "reservation_number",
            "raw_data",
            "received_at",
            "processing_status",
            "processing_error",
        ]

        read_only_fields = [
            "id",
            "received_at",
            "processing_status",
            "processing_error",
        ]