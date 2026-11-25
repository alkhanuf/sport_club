from datetime import date, time
from django.contrib.auth.models import User
from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient

from sportsclub.models import (
    SubscriptionType,
    ClientSubscription,
    Room,
    Schedule,
    Booking,
)


class RoomViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        room = baker.make(Room)

        r = self.client.get("/api/Room/")
        data = r.json()

        assert r.status_code == 200
        assert len(data) == 1
        assert data[0]["id"] == room.id
        assert data[0]["name"] == room.name

    def test_create_room(self):
        r = self.client.post("/api/Room/", {"name": "Зал йоги"})
        assert r.status_code == 201

        new_id = r.json()["id"]
        rooms = Room.objects.all()
        assert len(rooms) == 1

        new_room = Room.objects.filter(id=new_id).first()
        assert new_room.name == "Зал йоги"

    def test_update_room(self):
        rooms = baker.make(Room, 5)
        room = rooms[0]

        r = self.client.put(f"/api/Room/{room.id}/", {"name": "Новый зал"})
        assert r.status_code == 200

        room.refresh_from_db()
        assert room.name == "Новый зал"
        assert r.json()["name"] == "Новый зал"

    def test_delete_room(self):
        rooms = baker.make(Room, 10)
        r = self.client.get("/api/Room/")
        assert len(r.json()) == 10

        room_id = rooms[3].id
        r = self.client.delete(f"/api/Room/{room_id}/")
        assert r.status_code == 204

        r = self.client.get("/api/Room/")
        data = r.json()
        assert len(data) == 9
        assert room_id not in [i["id"] for i in data]

class SubscriptionTypeViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        sub_type = baker.make(SubscriptionType)

        r = self.client.get("/api/Subscription_Type/")
        data = r.json()

        assert r.status_code == 200
        assert len(data) == 1
        assert data[0]["id"] == sub_type.id
        assert data[0]["name"] == sub_type.name

    def test_create_subscription_type(self):
        r = self.client.post("/api/Subscription_Type/", {
            "name": "Базовый",
            "description": "Посещение зала",
            "base_cost": 2500.0,
            "validity_period": 30,
            "is_active": True,
        })
        assert r.status_code == 201

        new_id = r.json()["id"]
        sub_type = SubscriptionType.objects.filter(id=new_id).first()
        assert sub_type.name == "Базовый"
        assert sub_type.base_cost == 2500.0

    def test_update_subscription_type(self):
        sub_types = baker.make(SubscriptionType, 5)
        sub_type = sub_types[0]

        r = self.client.put(f"/api/Subscription_Type/{sub_type.id}/", {
            "name": "Максимум",
            "description": sub_type.description,
            "base_cost": 4000.0,
            "validity_period": sub_type.validity_period,
            "is_active": sub_type.is_active,
        })
        assert r.status_code == 200

        sub_type.refresh_from_db()
        assert sub_type.name == "Максимум"
        assert sub_type.base_cost == 4000.0

    def test_delete_subscription_type(self):
        sub_types = baker.make(SubscriptionType, 10)
        sub_type_id = sub_types[4].id

        r = self.client.delete(f"/api/Subscription_Type/{sub_type_id}/")
        assert r.status_code == 204

        data = self.client.get("/api/Subscription_Type/").json()
        assert len(data) == 9
        assert sub_type_id not in [i["id"] for i in data]


class ClientSubscriptionViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        user = baker.make(User)
        sub_type = baker.make(SubscriptionType)
        sub = baker.make(ClientSubscription, user=user, subscription_type=sub_type)

        r = self.client.get("/api/Client_Subscription/")
        data = r.json()

        assert r.status_code == 200
        assert len(data) == 1
        assert data[0]["id"] == sub.id
        assert data[0]["user"] == user.id
        assert data[0]["subscription_type"] == sub_type.id

    def test_create_client_subscription(self):
        user = baker.make(User)
        sub_type = baker.make(SubscriptionType)

        r = self.client.post("/api/Client_Subscription/", {
            "user": user.id,
            "subscription_type": sub_type.id,
            "start_date": "2026-11-01",
            "end_date": "2026-12-01",
            "cost": 2500.0,
            "status": True,
        })
        assert r.status_code == 201

        new_id = r.json()["id"]
        sub = ClientSubscription.objects.filter(id=new_id).first()
        assert sub.user == user
        assert sub.subscription_type == sub_type
        assert sub.cost == 2500.0

    def test_update_client_subscription(self):
        subs = baker.make(ClientSubscription, 5)
        sub = subs[0]

        r = self.client.put(f"/api/Client_Subscription/{sub.id}/", {
            "user": sub.user.id,
            "subscription_type": sub.subscription_type.id,
            "start_date": str(sub.start_date),
            "end_date": str(sub.end_date),
            "cost": 3000.0,
            "status": False,
        })
        assert r.status_code == 200

        sub.refresh_from_db()
        assert sub.cost == 3000.0
        assert sub.status is False

    def test_delete_client_subscription(self):
        subs = baker.make(ClientSubscription, 10)
        sub_id = subs[1].id

        r = self.client.delete(f"/api/Client_Subscription/{sub_id}/")
        assert r.status_code == 204

        data = self.client.get("/api/Client_Subscription/").json()
        assert len(data) == 9
        assert sub_id not in [i["id"] for i in data]


class ScheduleViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        room = baker.make(Room)
        trainer = baker.make(User)
        sched = baker.make(Schedule, room=room, trainer=trainer)

        r = self.client.get("/api/Schedule/")
        data = r.json()

        assert r.status_code == 200
        assert len(data) == 1
        assert data[0]["id"] == sched.id
        assert data[0]["room"] == room.id
        assert data[0]["trainer"] == trainer.id

    def test_create_schedule(self):
        room = baker.make(Room)
        trainer = baker.make(User)

        r = self.client.post("/api/Schedule/", {
            "activity": "Кроссфит",
            "room": room.id,
            "trainer": trainer.id,
            "date": "2026-11-25",
            "time": "18:00:00",
            "status": True,
        })
        assert r.status_code == 201

        new_id = r.json()["id"]
        sched = Schedule.objects.filter(id=new_id).first()
        assert sched.activity == "Кроссфит"
        assert sched.room == room
        assert sched.trainer == trainer

    def test_update_schedule(self):
        schedules = baker.make(Schedule, 5)
        sched = schedules[0]

        r = self.client.put(f"/api/Schedule/{sched.id}/", {
            "activity": "Пилатес",
            "room": sched.room.id,
            "trainer": sched.trainer.id,
            "date": str(sched.date),
            "time": str(sched.time),
            "status": True,
        })
        assert r.status_code == 200

        sched.refresh_from_db()
        assert sched.activity == "Пилатес"

    def test_delete_schedule(self):
        schedules = baker.make(Schedule, 10)
        sched_id = schedules[5].id

        r = self.client.delete(f"/api/Schedule/{sched_id}/")
        assert r.status_code == 204

        data = self.client.get("/api/Schedule/").json()
        assert len(data) == 9
        assert sched_id not in [i["id"] for i in data]


class BookingViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        user = baker.make(User)
        sched = baker.make(Schedule)
        booking = baker.make(Booking, user=user, schedule=sched)

        r = self.client.get("/api/Booking/")
        data = r.json()

        assert r.status_code == 200
        assert len(data) == 1
        assert data[0]["id"] == booking.id
        assert data[0]["user"] == user.id
        assert data[0]["schedule"] == sched.id

    def test_create_booking(self):
        user = baker.make(User)
        sched = baker.make(Schedule)

        r = self.client.post("/api/Booking/", {
            "user": user.id,
            "schedule": sched.id,
        })
        assert r.status_code == 201

        new_id = r.json()["id"]
        booking = Booking.objects.filter(id=new_id).first()
        assert booking.user == user
        assert booking.schedule == sched

    def test_update_booking(self):
        bookings = baker.make(Booking, 5)
        booking = bookings[0]
        new_sched = baker.make(Schedule)

        r = self.client.put(f"/api/Booking/{booking.id}/", {
            "user": booking.user.id,
            "schedule": new_sched.id,
        })
        assert r.status_code == 200

        booking.refresh_from_db()
        assert booking.schedule == new_sched

    def test_delete_booking(self):
        bookings = baker.make(Booking, 10)
        booking_id = bookings[6].id

        r = self.client.delete(f"/api/Booking/{booking_id}/")
        assert r.status_code == 204

        data = self.client.get("/api/Booking/").json()
        assert len(data) == 9
        assert booking_id not in [i["id"] for i in data]


class UserViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        user = baker.make(User)

        r = self.client.get("/api/User/")
        data = r.json()

        assert r.status_code == 200
        assert len(data) == 1
        assert data[0]["id"] == user.id
        assert data[0]["username"] == user.username

    def test_create_user(self):
        r = self.client.post("/api/User/", {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Тест",
            "last_name": "Юзер",
        })
        assert r.status_code == 201

        new_id = r.json()["id"]
        user = User.objects.filter(id=new_id).first()
        assert user.username == "testuser"

    def test_update_user(self):
        users = baker.make(User, 5)
        user = users[0]

        r = self.client.put(f"/api/User/{user.id}/", {
            "username": "updated_user",
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })
        assert r.status_code == 200

        user.refresh_from_db()
        assert user.username == "updated_user"

    def test_delete_user(self):
        users = baker.make(User, 10)
        user_id = users[7].id

        r = self.client.delete(f"/api/User/{user_id}/")
        assert r.status_code == 204

        data = self.client.get("/api/User/").json()
        assert len(data) == 9
        assert user_id not in [i["id"] for i in data]