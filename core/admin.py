from django.contrib import admin
from .models import (
    Resort,
    Department,
    Guest,
    Room,
    Reservation,
    Payment,
)


admin.site.register(Resort)
admin.site.register(Department)
admin.site.register(Guest)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Payment)