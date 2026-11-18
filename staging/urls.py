from django.urls import path

from .views import (
    ReservationIngestionAPIView
)


urlpatterns = [

    path(
        "reservations/",
        ReservationIngestionAPIView.as_view(),
        name="reservation-ingestion"
    ),

]