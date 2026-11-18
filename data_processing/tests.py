
from datetime import date
from django.test import SimpleTestCase

from .mappers import map_booking_status
from .transformers import transform_amount, transform_date, transform_name
from .validators import validate_reservation


class ReservationValidationTests(SimpleTestCase):
    def setUp(self):
        self.valid_payload = {
            "reservation_number": "TEST-001",
            "guest": "Guest Example",
            "resort": "ET01",
            "check_in": "01/10/26",
            "check_out": "03/10/26",
            "booking_status": "CO",
            "amount": "NAD 1,200.50",
        }

    def test_valid_payload_passes_validation(self):
        self.assertEqual(validate_reservation(self.valid_payload), [])

    def test_reversed_dates_fail_validation(self):
        payload = {**self.valid_payload, "check_in": "03/10/26", "check_out": "01/10/26"}
        self.assertIn("Check-out must be after check-in.", validate_reservation(payload))

    def test_negative_amount_fails_validation(self):
        payload = {**self.valid_payload, "amount": "-1"}
        self.assertIn("Amount cannot be negative.", validate_reservation(payload))

    def test_rooms_booked_defaults_to_one(self):
        self.assertEqual(validate_reservation(self.valid_payload), [])

    def test_transformers_normalize_values(self):
        self.assertEqual(transform_name("  maria   garcia "), "Maria Garcia")
        self.assertEqual(transform_date("2026-10-01"), date(2026, 10, 1))
        self.assertEqual(str(transform_amount("NAD 1,200.50")), "1200.50")
        self.assertEqual(map_booking_status(" co "), "Checked Out")
