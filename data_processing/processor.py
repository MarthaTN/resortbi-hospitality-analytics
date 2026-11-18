from django.db import transaction

from .pipeline import process_reservation
from staging.models import StagedReservation
from warehouse.models import TrustedReservation


@transaction.atomic
def process_staged_reservation(staged_reservation):

    raw_data = staged_reservation.raw_data

    result = process_reservation(raw_data)

    if result["status"] == "VALID":

        processed_data = result["data"]

        TrustedReservation.objects.update_or_create(
            staged_reservation=staged_reservation,

            defaults={
                "reservation_number": (
                    processed_data["reservation_number"]
                ),

                "guest_name": processed_data["guest"],

                "country": processed_data["country"],

                "resort_name": processed_data["resort"],

                "check_in": processed_data["check_in"],

                "check_out": processed_data["check_out"],

                "booking_status": (
                    processed_data["booking_status"]
                ),
                "rooms_booked": processed_data["rooms_booked"],

                "amount": processed_data["amount"],
            }
        )

        staged_reservation.processing_status = "PROCESSED"
        staged_reservation.processing_error = ""

    else:

        staged_reservation.processing_status = "FAILED"

        staged_reservation.processing_error = "\n".join(
            result["errors"]
        )

    staged_reservation.save(
        update_fields=[
            "processing_status",
            "processing_error",
        ]
    )

    return result


def process_pending_reservations():

    pending_reservations = StagedReservation.objects.filter(
        processing_status="PENDING"
    )

    results = {
        "total": 0,
        "processed": 0,
        "failed": 0,
    }

    for staged_reservation in pending_reservations:

        result = process_staged_reservation(
            staged_reservation
        )

        results["total"] += 1

        if result["status"] == "VALID":
            results["processed"] += 1
        else:
            results["failed"] += 1

    return results