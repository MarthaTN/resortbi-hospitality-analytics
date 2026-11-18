RESORT_MAPPING = {
    "ET01": "Etosha Resort",
    "WT01": "Waterberg Resort",
    "SD01": "Sossus Dune Lodge",
}


BOOKING_STATUS_MAPPING = {
    "CN": "Confirmed",
    "CI": "Checked In",
    "CO": "Checked Out",
    "CA": "Cancelled",
}


def map_resort(resort_code):
    return RESORT_MAPPING.get(resort_code)


def map_booking_status(status_code):
    return BOOKING_STATUS_MAPPING.get(str(status_code).strip().upper()) if status_code is not None else None