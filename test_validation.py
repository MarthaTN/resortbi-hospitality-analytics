from datetime import date

from data_processing.validators import validate_reservation


valid_reservation = {
    "reservation_number": "RES-2001",
    "guest": "Maria Garcia",
    "resort": "Etosha Resort",
    "check_in": date(2026, 9, 13),
    "check_out": date(2026, 9, 15),
    "amount": 4800,
    "booking_status": "CO"
}


invalid_reservation = {
    "reservation_number": "",
    "guest": "Maria Garcia",
    "resort": "Etosha Resort",
    "check_in": date(2026, 9, 15),
    "check_out": date(2026, 9, 13),
    "amount": -4800,
    "booking_status": "CO"
}


print("VALID RESERVATION")
print(validate_reservation(valid_reservation))

print("\nINVALID RESERVATION")
print(validate_reservation(invalid_reservation))