from django.urls import path, include
from rest_framework import routers

from airport.views import (
    CrewViewSet,
    AirplaneTypeViewSet,
    OrderViewSet,
    AirplaneViewSet,
    AirportViewSet,
    RouteViewSet,
    FlightViewSet,
)

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("orders", OrderViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("flights", FlightViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
