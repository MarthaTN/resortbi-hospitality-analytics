
from datetime import date
from decimal import Decimal

from django.test import TestCase

from staging.models import StagedReservation
from warehouse.models import TrustedReservation
from analytics.services.visitors import get_visitor_summary


class VisitorAnalyticsTestCase(TestCase):
    def add_reservation(self, number, country):
        staged = StagedReservation.objects.create(
            source_system="TEST", reservation_number=number, raw_data={}
        )
        TrustedReservation.objects.create(
            staged_reservation=staged,
            reservation_number=number,
            guest_name="Test Guest",
            country=country,
            resort_name="Etosha Resort",
            check_in=date(2026, 10, 1),
            check_out=date(2026, 10, 2),
            booking_status="Checked Out",
            rooms_booked=1,
            amount=Decimal("100.00"),
        )

    def test_unknown_country_is_not_classified_as_foreign(self):
        self.add_reservation("VIS-001", "Namibia")
        self.add_reservation("VIS-002", "South Africa")
        self.add_reservation("VIS-003", "")
        result = get_visitor_summary(date(2026, 10, 1), date(2026, 10, 1))
        self.assertEqual(result["total_reservations"], 3)
        self.assertEqual(result["namibian_reservations"], 1)
        self.assertEqual(result["foreign_reservations"], 1)
        self.assertEqual(result["unknown_country_reservations"], 1)
