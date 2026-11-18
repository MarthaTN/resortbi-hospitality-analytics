from django.db import models



class Resort(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True)
    region = models.CharField(max_length=100, blank=True)
    resort_type = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Guest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Room(models.Model):
    resort = models.ForeignKey(
        Resort,
        on_delete=models.PROTECT,
        related_name="rooms"
    )
    room_number = models.CharField(max_length=50)
    room_type = models.CharField(max_length=100, blank=True)
    capacity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.resort.name} - {self.room_number}"

class Reservation(models.Model):
    reservation_number = models.CharField(
        max_length=100,
        unique=True
    )
    guest = models.ForeignKey(
        Guest,
        on_delete=models.PROTECT,
        related_name="reservations"
    )
    resort = models.ForeignKey(
        Resort,
        on_delete=models.PROTECT,
        related_name="reservations"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="reservations",
        null=True,
        blank=True
    )
    check_in = models.DateField()
    check_out = models.DateField()
    booking_status = models.CharField(max_length=50)
    booking_source = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reservation_number

class Payment(models.Model):
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.PROTECT,
        related_name="payments"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    currency = models.CharField(max_length=10, default="NAD")
    payment_method = models.CharField(max_length=50, blank=True)
    payment_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.amount} {self.currency}"

    

class TrustedReservation(models.Model):
    staged_reservation = models.OneToOneField(
        "staging.StagedReservation",
        on_delete=models.PROTECT,
        related_name="trusted_reservation"
    )

    reservation_number = models.CharField(max_length=100)

    guest_name = models.CharField(max_length=200)

    country = models.CharField(max_length=100, blank=True)

    resort_name = models.CharField(max_length=150)

    check_in = models.DateField()

    check_out = models.DateField()

    booking_status = models.CharField(max_length=50)

    rooms_booked = models.PositiveIntegerField(
    default=1
)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    processed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.reservation_number