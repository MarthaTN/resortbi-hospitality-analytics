
from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, Sum

from warehouse.models import TrustedReservation

# These are the known statuses mapped by data_processing/mappers.py.
# Cancelled reservations are not counted as reservation value.
COUNTED_BOOKING_STATUSES = ("Confirmed", "Checked In", "Checked Out")


def _base_queryset(resort_name=None):
    queryset = TrustedReservation.objects.filter(
        booking_status__in=COUNTED_BOOKING_STATUSES
    )
    if resort_name:
        queryset = queryset.filter(resort_name__iexact=resort_name)
    return queryset


def get_revenue_summary(start_date=None, end_date=None, resort_name=None):
    """Summarize reservation amounts by check-in date.

    IMPORTANT: amount is the amount stored on a reservation, not verified
    payment/collection data. Present this metric as 'Reservation value'
    until payment data is integrated and reconciled.
    """
    queryset = _base_queryset(resort_name)

    if start_date:
        queryset = queryset.filter(check_in__gte=start_date)
    if end_date:
        queryset = queryset.filter(check_in__lte=end_date)

    summary = queryset.aggregate(
        total_revenue=Sum("amount"),
        reservation_count=Count("id"),
    )
    total_value = summary["total_revenue"] or Decimal("0.00")

    value_by_resort = (
        queryset.values("resort_name")
        .annotate(
            total_revenue=Sum("amount"),
            reservation_count=Count("id"),
        )
        .order_by("-total_revenue")
    )

    return {
        "total_revenue": str(total_value),
        "reservation_count": summary["reservation_count"] or 0,
        "revenue_by_resort": [
            {
                "resort_name": row["resort_name"],
                "total_revenue": str(row["total_revenue"] or Decimal("0.00")),
                "reservation_count": row["reservation_count"],
            }
            for row in value_by_resort
        ],
        "metric_definition": (
            "Sum of reservation amounts by check-in date; not verified "
            "cash collected or accounting revenue."
        ),
    }


def get_revenue_comparison(start_date, end_date, resort_name=None):
    """Compare inclusive date ranges of equal length."""
    if start_date > end_date:
        raise ValueError("start_date cannot be after end_date.")

    period_length = (end_date - start_date).days + 1
    previous_end_date = start_date - timedelta(days=1)
    previous_start_date = previous_end_date - timedelta(days=period_length - 1)

    queryset = _base_queryset(resort_name)

    current_value = queryset.filter(
        check_in__gte=start_date,
        check_in__lte=end_date,
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    previous_value = queryset.filter(
        check_in__gte=previous_start_date,
        check_in__lte=previous_end_date,
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    difference = current_value - previous_value
    percentage_change = (
        (difference / previous_value) * 100
        if previous_value != 0
        else None
    )

    return {
        "current_period": {
            "start_date": start_date,
            "end_date": end_date,
            "revenue": str(current_value),
        },
        "previous_period": {
            "start_date": previous_start_date,
            "end_date": previous_end_date,
            "revenue": str(previous_value),
        },
        "difference": str(difference),
        "percentage_change": (
            str(percentage_change.quantize(Decimal("0.01")))
            if percentage_change is not None
            else None
        ),
        "metric_definition": (
            "Comparison of reservation amounts by check-in date, not "
            "verified cash collected or accounting revenue."
        ),
    }
