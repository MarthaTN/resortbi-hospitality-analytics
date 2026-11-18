from datetime import datetime
from decimal import Decimal


def transform_name(name):
    if not name:
        return ""

    return " ".join(name.strip().title().split())


def transform_country(country):
    if not country:
        return ""

    return country.strip().title()


def transform_date(date_value):
    if not date_value:
        return None

    if isinstance(date_value, datetime):
        return date_value.date()

    if hasattr(date_value, "year"):
        return date_value

    cleaned = date_value.strip()
    for date_format in ("%d/%m/%y", "%Y-%m-%d"):
        try:
            return datetime.strptime(cleaned, date_format).date()
        except ValueError:
            continue
    raise ValueError("Date must use DD/MM/YY or YYYY-MM-DD format.")


def transform_rooms_booked(value):
    if value is None:
        return 1

    return int(value)

def transform_amount(amount):
    if amount is None:
        return Decimal("0.00")

    if isinstance(amount, (int, float, Decimal)):
        return Decimal(str(amount))

    cleaned_amount = (
        amount.upper()
        .replace("NAD", "")
        .replace(",", "")
        .strip()
    )

    return Decimal(cleaned_amount).quantize(
        Decimal("0.01")
    )