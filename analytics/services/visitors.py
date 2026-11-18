
from warehouse.models import TrustedReservation

COUNTED_BOOKING_STATUSES = ("Confirmed", "Checked In", "Checked Out")


def get_visitor_summary(start_date=None, end_date=None, resort_name=None):
    """Count reservation records by country; this is not guest headcount."""
    queryset = TrustedReservation.objects.filter(
        booking_status__in=COUNTED_BOOKING_STATUSES
    )

    if start_date:
        queryset = queryset.filter(check_in__gte=start_date)
    if end_date:
        queryset = queryset.filter(check_in__lte=end_date)
    if resort_name:
        queryset = queryset.filter(resort_name__iexact=resort_name)

    namibian = queryset.filter(country__iexact="Namibia").count()
    foreign = queryset.exclude(country__iexact="Namibia").exclude(
        country__isnull=True
    ).exclude(country__exact="").count()
    unknown = queryset.filter(country__exact="").count()

    return {
        "total_reservations": queryset.count(),
        "namibian_reservations": namibian,
        "foreign_reservations": foreign,
        "unknown_country_reservations": unknown,
        "metric_definition": (
            "Counts reservation records by guest country. It does not "
            "represent unique guests or total people travelling."
        ),
    }
