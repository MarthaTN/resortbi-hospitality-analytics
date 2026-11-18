
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsAnalyticsUser, IsManagement
from .services.alerts import generate_revenue_alert
from .services.dashboard import get_dashboard_summary
from .services.occupancy import get_occupancy_summary
from .services.revenue import get_revenue_comparison, get_revenue_summary
from .services.visitors import get_visitor_summary


def _parse_date(value, field_name, required=False):
    if not value:
        if required:
            raise ValueError(f"{field_name} is required.")
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD format.") from exc


def _get_filters(request, require_dates=False):
    start_text = request.query_params.get("start_date")
    end_text = request.query_params.get("end_date")
    start_date = _parse_date(start_text, "start_date", require_dates)
    end_date = _parse_date(end_text, "end_date", require_dates)
    if start_date and end_date and start_date > end_date:
        raise ValueError("start_date cannot be after end_date.")
    return (
        start_text or None,
        end_text or None,
        start_date,
        end_date,
        request.query_params.get("resort_name") or None,
    )


class AnalyticsAPIView(APIView):
    permission_classes = [IsAnalyticsUser]
    require_dates = True

    def get_data(self, start_date, end_date, resort_name):
        raise NotImplementedError

    def get(self, request):
        try:
            start_text, end_text, start_date, end_date, resort_name = _get_filters(
                request, self.require_dates
            )
            data = self.get_data(start_date, end_date, resort_name)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "filters": {
                "start_date": start_text,
                "end_date": end_text,
                "resort_name": resort_name,
            },
            "data": data,
        })


class RevenueSummaryAPIView(AnalyticsAPIView):
    permission_classes = [IsManagement]
    require_dates = False

    def get_data(self, start_date, end_date, resort_name):
        return get_revenue_summary(start_date, end_date, resort_name)


class RevenueComparisonAPIView(AnalyticsAPIView):
    permission_classes = [IsManagement]

    def get_data(self, start_date, end_date, resort_name):
        return get_revenue_comparison(start_date, end_date, resort_name)


class OccupancySummaryAPIView(AnalyticsAPIView):
    def get_data(self, start_date, end_date, resort_name):
        return get_occupancy_summary(start_date, end_date, resort_name)


class VisitorSummaryAPIView(AnalyticsAPIView):
    require_dates = False

    def get_data(self, start_date, end_date, resort_name):
        return get_visitor_summary(start_date, end_date, resort_name)


class DashboardSummaryAPIView(AnalyticsAPIView):
    permission_classes = [IsManagement]

    def get_data(self, start_date, end_date, resort_name):
        return get_dashboard_summary(start_date, end_date, resort_name)


class RevenueAlertAPIView(AnalyticsAPIView):
    permission_classes = [IsManagement]

    def get_data(self, start_date, end_date, resort_name):
        return {"alert": generate_revenue_alert(start_date, end_date, resort_name)}
