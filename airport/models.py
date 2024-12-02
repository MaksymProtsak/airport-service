from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="departing_routes",
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="arriving_routes",
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} → {self.destination} ({self.distance} km)"

    @staticmethod
    def validate_route(destination, distance, source):
        errors = {}
        if Route.objects.filter(
                destination=destination,
                distance=distance
        ).exists():
            errors["route_exist"] = "The route already exist."
            return errors["route_exist"]
        elif destination == source:
            errors["destination_equal"] = "The destination and source are equal."
            return errors["destination_equal"]
        return errors

    def clean(self):
        Route.validate_route(
            self.destination,
            self.distance,
            self.source,
        )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('source', 'destination')


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    @staticmethod
    def validate_route(
            route,
            airplane,
            departure_time,
            arrival_time
    ):
        errors = {}
        breakpoint()
        if Flight.objects.filter(
                route=route,
                airplane=airplane,
                departure_time=departure_time,
                arrival_time=arrival_time,
        ):
            errors["route_exist"] = (
                f"Flight with route '{route}'already exist."
            )
        elif departure_time == arrival_time:
            errors["departure_time"] = (
                "The departure time and arrival time cannot be same."
            )
        return errors

    def __str__(self):
        return (
            f"{self.route}, "
            f"{self.airplane}, "
            f"{self.departure_time}, "
            f"{self.arrival_time}."
        )

    def clean(self):
        Flight.validate_route(
            self.route,
            self.airplane,
            self.departure_time,
            self.arrival_time,
        )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    @staticmethod
    def validate_ticket(row, seat, flight): # Finish validation method
        errors = {}
        if Ticket.objects.filter(
                row=row,
                seat=seat,
                flight=flight,
        ):
            errors["route_exist"] = (
                f"The place 'seat: {seat}, row: {row}' "
                f"with flight '{flight}' already bought."
            )
        return errors

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight,
        )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.flight}, row: {self.row}, seat: {self.seat}."
