
from datetime import timedelta

from core.models import Room
from warehouse.models import TrustedReservation

COUNTED_BOOKING_STATUSES = ("Checked In", "Checked Out")


def get_occupancy_summary(start_date, end_date, resort_name=None):
    """Calculate occupancy as occupied room-nights / available room-nights.

    The requested start_date and end_date are inclusive. A reservation's
    check-out date is not an occupied night, following normal hotel practice.
    """
    if start_date > end_date:
        raise ValueError("start_date cannot be after end_date.")

    rooms = Room.objects.filter(is_active=True)
    if resort_name:
        rooms = rooms.filter(resort__name__iexact=resort_name)

    total_rooms = rooms.count()
    period_end_exclusive = end_date + timedelta(days=1)
    period_nights = (period_end_exclusive - start_date).days

    reservations = TrustedReservation.objects.filter(
        booking_status__in=COUNTED_BOOKING_STATUSES,
        check_in__lt=period_end_exclusive,
        check_out__gt=start_date,
    )
    if resort_name:
        reservations = reservations.filter(resort_name__iexact=resort_name)

    occupied_room_nights = 0
    for reservation in reservations.iterator():
        overlap_start = max(reservation.check_in, start_date)
        overlap_end = min(reservation.check_out, period_end_exclusive)
        nights_occupied = max(0, (overlap_end - overlap_start).days)
        occupied_room_nights += reservation.rooms_booked * nights_occupied

    available_room_nights = total_rooms * period_nights
    occupancy_rate = (
        occupied_room_nights / available_room_nights * 100
        if available_room_nights
        else 0
    )

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_rooms": total_rooms,
        "period_nights": period_nights,
        "occupied_room_nights": occupied_room_nights,
        "available_room_nights": available_room_nights,
        "occupancy_rate": round(occupancy_rate, 2),
        "metric_definition": (
            "Occupied room-nights divided by active-room available "
            "room-nights. Assumes active rooms were available throughout "
            "the selected period."
        ),
    }
