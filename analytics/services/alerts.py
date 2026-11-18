from decimal import Decimal

from .revenue import get_revenue_comparison


def generate_revenue_alert(
    start_date,
    end_date,
    resort_name=None,
    threshold=20
):

    comparison = get_revenue_comparison(
        start_date=start_date,
        end_date=end_date,
        resort_name=resort_name
    )

    percentage_change = comparison[
        "percentage_change"
    ]

    if percentage_change is None:
        return None

    percentage_change = Decimal(
        percentage_change
    )

    if percentage_change <= -Decimal(
        str(threshold)
    ):

        return {
            "type": "REVENUE_DECLINE",
            "severity": "HIGH",
            "message": (
                f"Reservation value decreased by "
                f"{abs(percentage_change)}% "
                f"compared with the previous "
                f"period."
            ),
            "percentage_change": str(
                percentage_change
            )
        }

    return None