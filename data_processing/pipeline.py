from .validators import validate_reservation
from .mappers import map_booking_status
from .transformers import (
    transform_name,
    transform_country,
    transform_date,
    transform_amount,
    transform_rooms_booked,
)

from core.models import Resort


def process_reservation(data):

    errors = validate_reservation(data)

    if errors:
        return {
            "status": "INVALID",
            "errors": errors,
            "data": None,
        }

    try:
        check_in = transform_date(
            data.get("check_in")
        )

        check_out = transform_date(
            data.get("check_out")
        )

        if not check_in or not check_out:
            return {
                "status": "INVALID",
                "errors": [
                    "Valid check-in and check-out dates are required."
                ],
                "data": None,
            }

        if check_out <= check_in:
            return {
                "status": "INVALID",
                "errors": [
                    "Check-out must be after check-in."
                ],
                "data": None,
            }

        resort = Resort.objects.filter(
            external_code=data.get("resort"),
            is_active=True
        ).first()

        if not resort:
            return {
                "status": "INVALID",
                "errors": [
                    "Resort does not exist or is inactive."
                ],
                "data": None,
            }

        mapped_status = map_booking_status(
            data.get("booking_status")
        )

        if not mapped_status:
            return {
                "status": "INVALID",
                "errors": [
                    "Unknown booking status."
                ],
                "data": None,
            }

        processed_data = {
            "reservation_number": data.get(
                "reservation_number"
            ),

            "guest": transform_name(
                data.get("guest")
            ),

            "country": transform_country(
                data.get("country")
            ),

            "resort": resort.name,

            "check_in": check_in,

            "check_out": check_out,

            "booking_status": mapped_status,
            "rooms_booked": transform_rooms_booked(
                data.get("rooms_booked")
            ),

            "amount": transform_amount(
                data.get("amount")
            ),

        }

        return {
            "status": "VALID",
            "errors": [],
            "data": processed_data,
        }

    except (ValueError, TypeError, ArithmeticError) as error:
        return {
            "status": "INVALID",
            "errors": [
                f"Processing error: {str(error)}"
            ],
            "data": None,
        }