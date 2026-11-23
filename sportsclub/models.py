from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.TextField("ФИО")
    email = models.EmailField("Email")
    phone_number = models.TextField("Номер телефона")
    birth_date = models.DateField("Дата рождения")
    date_of_registration = models.DateField("Дата регистрации", auto_now_add=True)
    gender  = models.TextField("Пол")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

class SubscriptionType(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание")
    base_cost = models.FloatField("Базовая стоимость")
    validity_period = models.IntegerField("Период действия")
    is_active = models.BooleanField("Активна", default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип абонемента"
        verbose_name_plural = "Типы абонементов"


class ClientSubscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    cost = models.FloatField("Стоимость")
    status = models.BooleanField("Статус", default=True)

    def __str__(self):
        return f'{self.client} — {self.subscription_type}'

    class Meta:
        verbose_name = "Абонемент клиента"
        verbose_name_plural = "Абонементы клиентов"


class Room(models.Model):
    name = models.TextField("Название")

    def __str__(self):
        return self.name



    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Залы"

class Trainer(models.Model):
    name = models.TextField("ФИО")
    phone_number = models.TextField("Номер телефона")
    gender = models.TextField("Пол")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"


class Schedule(models.Model):
    activity = models.TextField("Мероприятие")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    date = models.DateField("Дата")
    time = models.TimeField("Время")
    status = models.BooleanField("Статус", default=True)

    def __str__(self):
        return f'{self.activity} — {self.date}'

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"


class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.client} — {self.schedule}'

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
