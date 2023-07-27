from rest_framework import serializers
from .models import Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'login', 'password', 'passport', 'phone', 'email',  'address', 'role_id', 'referral_id',
                  'created_at', 'updated_at', 'deleted_at')
