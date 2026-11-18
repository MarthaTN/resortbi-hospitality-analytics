
from django.urls import path

from .views import (
    DashboardSummaryAPIView,
    OccupancySummaryAPIView,
    RevenueAlertAPIView,
    RevenueComparisonAPIView,
    RevenueSummaryAPIView,
    VisitorSummaryAPIView,
)

urlpatterns = [
    path("revenue/", RevenueSummaryAPIView.as_view(), name="revenue-summary"),
    path("revenue/comparison/", RevenueComparisonAPIView.as_view(), name="revenue-comparison"),
    path("occupancy/", OccupancySummaryAPIView.as_view(), name="occupancy-summary"),
    path("visitors/", VisitorSummaryAPIView.as_view(), name="visitor-summary"),
    path("dashboard/", DashboardSummaryAPIView.as_view(), name="dashboard-summary"),
    path("alerts/revenue/", RevenueAlertAPIView.as_view(), name="revenue-alert"),
]
