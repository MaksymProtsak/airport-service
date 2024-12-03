from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import (
    Crew,
    AirplaneType,
    Order,
    Airplane,
    Airport,
    Route,
    Flight,
    Ticket,
)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(RouteSerializer, self).validate(attrs=attrs)
        error = Route.validate_route(
            attrs["destination"],
            attrs["distance"],
            attrs["source"],
        )
        if error:
            raise ValidationError(error)
        return data

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class FlightSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(FlightSerializer, self).validate(attrs=attrs)
        error = Flight.validate_route(
            attrs["route"],
            attrs["airplane"],
            attrs["departure_time"],
            attrs["arrival_time"],
        )
        if error:
            raise ValidationError(error)
        return data

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time")


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        errors = Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"]
        )
        if errors:
            raise ValidationError(errors)
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at",)

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order
