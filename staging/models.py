from django.db import models


class StagedReservation(models.Model):
    source_system = models.CharField(max_length=100)

    reservation_number = models.CharField(max_length=100)

    raw_data = models.JSONField()

    received_at = models.DateTimeField(auto_now_add=True)

    processing_status = models.CharField(
        max_length=30,
        default="PENDING"
    )

    processing_error = models.TextField(blank=True)

    def __str__(self):
        return f"{self.source_system} - {self.reservation_number}"