from django.contrib.auth import authenticate

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
    email = serializers.EmailField()
    interest_sectors = serializers.JSONField()

    class Meta:
        model = Investor
        fields = ['email', 'password', 'password_confirmation', 'interest_sectors', 'investment_range', 'receive_interesting_offers']

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
        investor = Investor.objects.create(
            user=user,
            email=validated_data['email'],
            interest_sectors=validated_data['interest_sectors'],
            investment_range=validated_data['investment_range'],
            receive_interesting_offers=validated_data.get('receive_interesting_offers', False)
        )
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
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Учетная запись пользователя отключена.")
            else:
                raise serializers.ValidationError("Неверные учетные данные. Пожалуйста, попробуйте снова.")
        else:
            raise serializers.ValidationError("Для входа в систему необходимо предоставить адрес электронной почты и пароль.")

        attrs['user'] = user
        return attrs