from rest_framework import serializers
from .models import Users, Orders, Orders_fields_values


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'login', 'password', 'passport', 'phone', 'email',  'address', 'role_id', 'referral_id',
                  'created_at', 'updated_at', 'deleted_at')


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('id', 'user_id', 'type', 'address', 'square', 'packet_id',  'numbers_rooms', 'numbers_doors', 'numbers_toilets',
                  'created_at', 'updated_at', 'deleted_at')


class OrdersFieldsValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders_fields_values
        fields = ('id', 'order_id', 'orders_fields_id', 'value', 'size', 'created_at', 'updated_at', 'deleted_at')
