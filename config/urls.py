
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "application": "ResortBI",
        "description": "Hospitality Business Intelligence API",
        "status": "online",
        "message": "Welcome to the ResortBI API."
    })


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),

    path(
    "api/analytics/",
    include("analytics.urls")
),
path(
    "api/ingestion/",
    include("staging.urls")
),
path(
    "api/auth/token/",
    TokenObtainPairView.as_view(),
    name="token_obtain_pair",
),

path(
    "api/auth/token/refresh/",
    TokenRefreshView.as_view(),
    name="token_refresh",
),
path("api/auth/", include("accounts.urls")),
path(
        "api/",
        include("warehouse.urls")
    ),

]