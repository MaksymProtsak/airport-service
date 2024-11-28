from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import GenericViewSet

from airport.models import (
    Crew,
    AirplaneType,
)
from airport.serializer import (
    CrewSerializer,
    AirplaneTypeSerializer,
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
