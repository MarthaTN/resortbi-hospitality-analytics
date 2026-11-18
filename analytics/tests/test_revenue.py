
from datetime import date
from decimal import Decimal

from django.test import TestCase

from staging.models import StagedReservation
from warehouse.models import TrustedReservation
from ..services.revenue import get_revenue_summary, get_revenue_comparison


class RevenueAnalyticsTestCase(TestCase):
    def make_reservation(self, number, guest, country, resort, check_in, check_out, amount, status="Confirmed"):
        staged = StagedReservation.objects.create(
            source_system="TEST",
            reservation_number=number,
            raw_data={},
        )
        return TrustedReservation.objects.create(
            staged_reservation=staged,
            reservation_number=number,
            guest_name=guest,
            country=country,
            resort_name=resort,
            check_in=check_in,
            check_out=check_out,
            booking_status=status,
            rooms_booked=1,
            amount=Decimal(amount),
        )

    def setUp(self):
        self.make_reservation(
            "TEST-001", "Test Guest", "Namibia", "Etosha Resort",
            date(2026, 9, 10), date(2026, 9, 12), "3000.00",
        )
        self.make_reservation(
            "TEST-002", "Another Guest", "South Africa", "Waterberg Resort",
            date(2026, 9, 11), date(2026, 9, 13), "5000.00",
        )

    def test_total_reservation_value(self):
        result = get_revenue_summary()
        self.assertEqual(result["total_revenue"], "8000.00")
        self.assertEqual(result["reservation_count"], 2)

    def test_value_by_resort(self):
        result = get_revenue_summary()
        self.assertEqual(len(result["revenue_by_resort"]), 2)

    def test_date_filter_includes_both_boundaries(self):
        result = get_revenue_summary(
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 10),
        )
        self.assertEqual(result["total_revenue"], "3000.00")

    def test_resort_filter(self):
        result = get_revenue_summary(resort_name="Etosha Resort")
        self.assertEqual(result["total_revenue"], "3000.00")
        self.assertEqual(result["reservation_count"], 1)

    def test_cancelled_reservations_are_excluded(self):
        self.make_reservation(
            "TEST-003", "Cancelled Guest", "Namibia", "Etosha Resort",
            date(2026, 9, 10), date(2026, 9, 11), "900.00", status="Cancelled",
        )
        result = get_revenue_summary()
        self.assertEqual(result["total_revenue"], "8000.00")
        self.assertEqual(result["reservation_count"], 2)

    def test_comparison_periods_have_equal_inclusive_length(self):
        result = get_revenue_comparison(
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 11),
        )
        self.assertEqual(result["previous_period"]["start_date"], date(2026, 9, 8))
        self.assertEqual(result["previous_period"]["end_date"], date(2026, 9, 9))
