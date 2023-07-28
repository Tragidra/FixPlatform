from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Users, Orders, Orders_fields_values, Checks_fields, Work_stages


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'name', 'password', 'passport', 'phone', 'email', 'address', 'role_id', 'referral_id',
                  'created_at', 'updated_at', 'deleted_at')
        validators = [
            UniqueTogetherValidator(
                queryset=Users.objects.all(),
                fields=['phone', 'email']
            )
        ]


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = (
            'id', 'user_id', 'type', 'address', 'square', 'packet_id', 'numbers_rooms', 'numbers_doors',
            'numbers_toilets',
            'created_at', 'updated_at', 'deleted_at')


class OrdersFieldsValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders_fields_values
        fields = ('id', 'order_id', 'orders_fields_id', 'value', 'size', 'created_at', 'updated_at', 'deleted_at')


class Checks_fields_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Checks_fields
        fields = ('name', 'price', 'created_at', 'updated_at', 'deleted_at')


class Customers_payments_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Checks_fields
        fields = ('user_id', 'order_id', 'sum', 'status', 'number', 'created_at', 'updated_at', 'deleted_at')


class Work_stages_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Work_stages
        fields = ('text', 'created_at', 'updated_at', 'deleted_at')


class Orders_work_stages_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Work_stages
        fields = ('work_stages_id', 'order_id', 'status',  'created_at', 'updated_at', 'deleted_at')
