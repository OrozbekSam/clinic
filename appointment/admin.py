from django.contrib import admin
from appointment.models import Appointment, AppointmentItem


admin.site.register(Appointment)
admin.site.register(AppointmentItem)
