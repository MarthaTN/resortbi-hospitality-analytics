from data_processing.pipeline import process_reservation


valid_reservation = {
    "reservation_number": "RES-2001",
    "guest": "  anna shilongo ",
    "country": "   nAmIbIa   ",
    "resort": "ET01",
    "check_in": "10/09/26",
    "check_out": "12/09/26",
    "booking_status": "CO",
    "amount": "NAD 3,500",
}


invalid_reservation = {
    "reservation_number": "",
    "guest": "",
    "resort": "",
    "check_in": "12/09/26",
    "check_out": "10/09/26",
    "booking_status": "CO",
    "amount": "-500",
}


print("VALID RESERVATION")
print(process_reservation(valid_reservation))

print("\nINVALID RESERVATION")
print(process_reservation(invalid_reservation))