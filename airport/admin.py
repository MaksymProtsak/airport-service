from django.contrib import admin

from .models import (
    Crew,
    AirplaneType,
    Order,
    Airplane,
    Airport,
    Route,
    Flight,
    Ticket,
)

admin.site.register(Crew)
admin.site.register(AirplaneType)
admin.site.register(Order)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(Ticket)
