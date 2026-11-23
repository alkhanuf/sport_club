from django.contrib import admin
from .models import SubscriptionType, ClientSubscription, Room, Trainer, Schedule, Booking


@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'base_cost', 'validity_period', 'is_active')


@admin.register(ClientSubscription)
class ClientSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subscription_type', 'start_date', 'end_date', 'cost', 'status')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'gender')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'activity', 'room', 'trainer', 'date', 'time', 'status')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'schedule')