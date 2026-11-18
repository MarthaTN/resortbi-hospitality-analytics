
from datetime import date, datetime
from decimal import Decimal, InvalidOperation


def validate_reservation(data):
    if not isinstance(data, dict):
        return ["Reservation payload must be a JSON object."]

    errors = []
    required_fields = (
        "reservation_number",
        "guest",
        "resort",
        "check_in",
        "check_out",
        "booking_status",
        "amount",
    )

    for field in required_fields:
        value = data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(f"{field} is required.")

    check_in = data.get("check_in")
    check_out = data.get("check_out")

    def as_date(value):
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        if isinstance(value, str) and value.strip():
            for date_format in ("%d/%m/%y", "%Y-%m-%d"):
                try:
                    return datetime.strptime(value.strip(), date_format).date()
                except ValueError:
                    continue
        return None

    parsed_in = as_date(check_in)
    parsed_out = as_date(check_out)
    if check_in and parsed_in is None:
        errors.append("check_in must use DD/MM/YY or YYYY-MM-DD format.")
    if check_out and parsed_out is None:
        errors.append("check_out must use DD/MM/YY or YYYY-MM-DD format.")
    if parsed_in and parsed_out and parsed_out <= parsed_in:
        errors.append("Check-out must be after check-in.")

    amount = data.get("amount")
    if amount not in (None, ""):
        try:
            cleaned_amount = str(amount).upper().replace("NAD", "").replace(",", "").strip()
            parsed_amount = Decimal(cleaned_amount)
            if not parsed_amount.is_finite():
                raise InvalidOperation
            if parsed_amount < 0:
                errors.append("Amount cannot be negative.")
        except (InvalidOperation, ValueError, TypeError):
            errors.append("Amount must be a valid number.")

    rooms_booked = data.get("rooms_booked", 1)
    try:
        parsed_rooms = int(rooms_booked)
        if parsed_rooms <= 0:
            errors.append("Rooms booked must be greater than zero.")
    except (ValueError, TypeError):
        errors.append("Rooms booked must be a valid whole number.")

    return errors
