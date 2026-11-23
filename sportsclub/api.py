from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from sportsclub.serializers import (
    UserSerializer,
    SubscriptionTypeSerializer,
    ClientSubscriptionSerializer,
    RoomSerializer,
    TrainerSerializer,
    ScheduleSerializer,
    BookingSerializer,
)
from sportsclub.models import SubscriptionType, ClientSubscription, Room, Trainer, Schedule, Booking


class UsersViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SubscriptionTypeViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer


class ClientSubscriptionViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = ClientSubscription.objects.all()
    serializer_class = ClientSubscriptionSerializer


class RoomViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class TrainerViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer


class ScheduleViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class BookingViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer