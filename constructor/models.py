from datetime import datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

now = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")


class Users(models.Model):
    name = models.TextField()
    password = models.TextField()
    passport = models.TextField(null=True)
    phone = models.BigIntegerField()
    email = models.TextField()
    address = models.TextField()
    role_id = models.IntegerField()
    referral_id = models.IntegerField(null=True)
    bonus = models.FloatField(default=0.00)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


class Orders(models.Model):
    user_id = models.IntegerField()
    type = models.IntegerField()  # 1 - квартира, 2 - дом
    address = models.TextField()
    square = models.FloatField()
    packet_id = models.IntegerField()
    numbers_rooms = models.IntegerField()
    numbers_doors = models.IntegerField()
    numbers_toilets = models.IntegerField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


class Orders_fields(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


class Orders_fields_values(models.Model):
    order_id = models.IntegerField()
    orders_fields_id = models.IntegerField()
    value = models.TextField()
    size = models.FloatField(null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


class Checks_fields(models.Model):
    name = models.TextField()  # Сами опции в формате id - имя
    price = models.IntegerField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


class Orders_checks_fields_values(models.Model):  # Клиент вбивает исключительно объём, value = объём
    order_id = models.IntegerField()
    check_field_id = models.IntegerField()
    value = models.TextField()  # Сами опции в формате id - имя
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


class Roles(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


class Repair_packets(models.Model):
    name = models.TextField()
    price = models.IntegerField()
    # тут будут ещё скорее всего что-то по типу base_options_id и т.п.
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


# class Installation_works(models.Model):
#     name = models.TextField()
#     price = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField(null=True)
#     deleted_at = models.DateTimeField(null=True)


# class Dismantling_works(models.Model):
#     name = models.TextField()
#     price = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField(null=True)
#     deleted_at = models.DateTimeField(null=True)
#
#
# class Additional_options(models.Model):
#     name = models.TextField()
#     price = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField(null=True)
#     deleted_at = models.DateTimeField(null=True)
#
#
# class Additional_works(models.Model):
#     name = models.TextField()
#     price = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField(null=True)
#     deleted_at = models.DateTimeField(null=True)


class Chats(models.Model):
    client_id = models.IntegerField()
    manager_id = models.IntegerField()
    chat_texts_id = models.IntegerField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


class Chat_texts(models.Model):
    chat_id = models.IntegerField()
    text = models.TextField()
    autor = models.IntegerField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


class Customers_payments(models.Model):  # Подразумевается, что оплаты будут сразу создаваться при оформлении заказа
    user_id = models.IntegerField()
    order_id = models.IntegerField()
    sum = models.FloatField(default=0)
    status = models.TextField(default='created')
    number = models.IntegerField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


class Files(models.Model):  # Фогографии с объектов
    order_id = models.IntegerField()
    path = models.TextField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


class Work_stages(models.Model):  # Всевозможные этапы работ
    text = models.TextField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


class Orders_work_stages(models.Model):  # Всевозможные этапы работ
    work_stages_id = models.IntegerField()
    order_id = models.IntegerField()
    status = models.TextField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)



