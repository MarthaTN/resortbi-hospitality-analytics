
from .alerts import generate_revenue_alert
from .occupancy import get_occupancy_summary
from .revenue import get_revenue_summary
from .visitors import get_visitor_summary


def get_dashboard_summary(start_date, end_date, resort_name=None):
    return {
        "revenue": get_revenue_summary(
            start_date=start_date,
            end_date=end_date,
            resort_name=resort_name,
        ),
        "occupancy": get_occupancy_summary(
            start_date=start_date,
            end_date=end_date,
            resort_name=resort_name,
        ),
        "visitors": get_visitor_summary(
            start_date=start_date,
            end_date=end_date,
            resort_name=resort_name,
        ),
        "revenue_alert": generate_revenue_alert(
            start_date=start_date,
            end_date=end_date,
            resort_name=resort_name,
        ),
    }
