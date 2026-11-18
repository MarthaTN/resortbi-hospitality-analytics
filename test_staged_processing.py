import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from staging.models import StagedReservation
from data_processing.processor import process_staged_reservation


staged_reservation = StagedReservation.objects.get(
    reservation_number="RES-2001"
)

result = process_staged_reservation(staged_reservation)

print(result)
print("Processing status:", staged_reservation.processing_status)