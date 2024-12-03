from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import GenericViewSet

from airport.models import (
    Crew,
    AirplaneType,
    Order,
    Airport,
    Airplane,
    Flight,
    Route,
    Ticket,
)
from airport.serializers import (
    CrewSerializer,
    AirplaneTypeSerializer,
    OrderSerializer,
    AirportSerializer,
    AirplaneSerializer,
    RouteSerializer,
    FlightSerializer,
    TicketSerializer,
)


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    def list(self, request, *args, **kwargs):
        """Retrieve list of crews"""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new crew"""
        return super().create(request, *args, **kwargs)


class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer

    def list(self, request, *args, **kwargs):
        """Retrieve list of airplane types"""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new airplane type"""
        return super().create(request, *args, **kwargs)


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """Retrieve list of orders"""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new order"""
        return super().create(request, *args, **kwargs)


class AirplaneViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

    def list(self, request, *args, **kwargs):
        """Retrieve list of airplanes"""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new irplane"""
        return super().create(request, *args, **kwargs)


class AirportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

    def list(self, request, *args, **kwargs):
        """Retrieve list of airports"""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new airport"""
        return super().create(request, *args, **kwargs)


class RouteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def list(self, request, *args, **kwargs):
        """Retrieve list of routes"""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new route"""
        return super().create(request, *args, **kwargs)


class FlightViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def list(self, request, *args, **kwargs):
        """Retrieve list of flights"""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new flight"""
        return super().create(request, *args, **kwargs)
