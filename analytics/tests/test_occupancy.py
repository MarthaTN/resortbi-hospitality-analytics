
from datetime import date
from decimal import Decimal

from django.test import TestCase

from core.models import Resort, Room
from staging.models import StagedReservation
from warehouse.models import TrustedReservation
from analytics.services.occupancy import get_occupancy_summary


class OccupancyAnalyticsTestCase(TestCase):
    def setUp(self):
        resort = Resort.objects.create(name="Etosha Resort", external_code="ET01")
        Room.objects.create(resort=resort, room_number="101")
        Room.objects.create(resort=resort, room_number="102")

    def add_reservation(self, number, check_in, check_out, rooms_booked=1, status="Checked Out"):
        staged = StagedReservation.objects.create(
            source_system="TEST", reservation_number=number, raw_data={}
        )
        return TrustedReservation.objects.create(
            staged_reservation=staged,
            reservation_number=number,
            guest_name="Test Guest",
            country="Namibia",
            resort_name="Etosha Resort",
            check_in=check_in,
            check_out=check_out,
            booking_status=status,
            rooms_booked=rooms_booked,
            amount=Decimal("100.00"),
        )

    def test_occupancy_uses_room_nights_not_reservation_total(self):
        self.add_reservation("OCC-001", date(2026, 10, 1), date(2026, 10, 3))
        result = get_occupancy_summary(date(2026, 10, 1), date(2026, 10, 2))
        self.assertEqual(result["occupied_room_nights"], 2)
        self.assertEqual(result["available_room_nights"], 4)
        self.assertEqual(result["occupancy_rate"], 50.0)

    def test_cancelled_reservation_is_not_counted(self):
        self.add_reservation(
            "OCC-002", date(2026, 10, 1), date(2026, 10, 3), status="Cancelled"
        )
        result = get_occupancy_summary(date(2026, 10, 1), date(2026, 10, 2))
        self.assertEqual(result["occupied_room_nights"], 0)
        self.assertEqual(result["occupancy_rate"], 0)


    def test_confirmed_booking_is_not_actual_occupancy(self):
        self.add_reservation(
            "OCC-003", date(2026, 10, 1), date(2026, 10, 3), status="Confirmed"
        )
        result = get_occupancy_summary(date(2026, 10, 1), date(2026, 10, 2))
        self.assertEqual(result["occupied_room_nights"], 0)

    def test_same_start_and_end_date_is_one_reporting_night(self):
        result = get_occupancy_summary(date(2026, 10, 1), date(2026, 10, 1))
        self.assertEqual(result["period_nights"], 1)
        self.assertEqual(result["available_room_nights"], 2)
