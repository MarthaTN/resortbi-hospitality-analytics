import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from data_processing.processor import (
    process_pending_reservations
)

result = process_pending_reservations()

print(result)