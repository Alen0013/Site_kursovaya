# bookings/admin.py
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'billiard_type', 'phone', 'created_at')
    list_filter = ('billiard_type', 'created_at')
    search_fields = ('name', 'surname', 'phone')