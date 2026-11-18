from rest_framework.routers import DefaultRouter

from .views import TrustedReservationViewSet
from django.contrib import admin
from django.urls import path, include



router = DefaultRouter()

router.register(
    "trusted-reservations",
    TrustedReservationViewSet,
    basename="trusted-reservation"
)

urlpatterns = router.urls

