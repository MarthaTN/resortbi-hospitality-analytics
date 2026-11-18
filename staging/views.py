from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permissions import IsAdministratorOrAnalyst

from .models import StagedReservation
from .serializers import StagedReservationSerializer

from data_processing.processor import (
    process_staged_reservation
)


class ReservationIngestionAPIView(APIView):

    permission_classes = [IsAdministratorOrAnalyst]

    def post(self, request):

        serializer = StagedReservationSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "status": "INVALID",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        raw_data = serializer.validated_data.get("raw_data")
        reservation_number = serializer.validated_data.get("reservation_number")
        if not isinstance(raw_data, dict):
            return Response(
                {
                    "status": "INVALID",
                    "errors": {"raw_data": ["Must be a JSON object containing reservation fields."]}
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        payload_number = raw_data.get("reservation_number")
        if payload_number and str(payload_number).strip() != str(reservation_number).strip():
            return Response(
                {
                    "status": "INVALID",
                    "errors": {"reservation_number": ["Must match raw_data.reservation_number."]}
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        staged_reservation = serializer.save()

        result = process_staged_reservation(
            staged_reservation
        )

        if result["status"] == "VALID":

            return Response(
                {
                    "status": "PROCESSED",
                    "message": (
                        "Reservation received "
                        "and processed successfully."
                    ),
                    "reservation_number":
                        staged_reservation.reservation_number,
                    "data": result["data"]
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "status": "FAILED",
                "reservation_number":
                    staged_reservation.reservation_number,
                "errors": result["errors"]
            },
            status=status.HTTP_400_BAD_REQUEST
        )