from .models import InterestSector, Investor, Businessman
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Investor


class InterestSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestSector
        fields = '__all__'


class InvestorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = Investor
        fields = ['email', 'password', 'password_confirmation', 'first_name', 'last_name', 'interest_sectors',
                  'investment_range', 'receive_interesting_offers', 'verification']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        user_data = {
            'username': validated_data['email'],  # Можете использовать email в качестве имени пользователя
            'email': validated_data['email'],
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
        }
        user = User.objects.create_user(**user_data)
        investor = Investor.objects.create(user=user, **validated_data)
        return investor

from rest_framework import serializers
from .models import Businessman, User


class BusinessmanRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    interest_sectors = serializers.JSONField()

    class Meta:
        model = Businessman
        fields = ['email', 'password', 'password_confirmation', 'interest_sectors', 'business_range', 'receive_interesting_offers']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        user_data = {
            'username': validated_data['email'],
            'email': validated_data['email'],
        }
        user = User.objects.create_user(**user_data)
        businessman = Businessman.objects.create(
            user=user,
            email=validated_data['email'],
            interest_sectors=validated_data['interest_sectors'],
            business_range=validated_data['business_range'],
            receive_interesting_offers=validated_data.get('receive_interesting_offers', False)
        )
        return businessman


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
