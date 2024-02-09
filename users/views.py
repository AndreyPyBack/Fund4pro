from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Investor, Businessman
from .serializers import UserLoginSerializer, BusinessmanRegistrationSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import InterestSector, Investor
from .serializers import InterestSectorSerializer, InvestorRegistrationSerializer

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class InterestSectorListCreateAPIView(APIView):
    def get(self, request):
        sectors = InterestSector.objects.all()
        serializer = InterestSectorSerializer(sectors, many=True)
        return Response(serializer.data)


class InvestorCreateAPIView(APIView):
    def post(self, request):
        serializer = InvestorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Попытка найти пользователя по email
            user, created = User.objects.get_or_create(
                email=serializer.validated_data['email'],
                defaults={
                    'username': serializer.validated_data['email'],
                    'password': serializer.validated_data['password'],
                    'first_name': serializer.validated_data.get('first_name', ''),
                    # Получаем данные о имени, если они были переданы
                    'last_name': serializer.validated_data.get('last_name', ''),
                    # Получаем данные о фамилии, если они были переданы
                }
            )
            # Если пользователь уже существует, возвращаем ошибку
            if not created:
                return Response({'error': 'Пользователь с таким email уже существует'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Создаем инвестора, связанного с пользователем
            investor = Investor.objects.create(
                user=user,
                interest_sectors=serializer.validated_data['interest_sectors'],
                investment_range=serializer.validated_data['investment_range'],
                receive_interesting_offers=serializer.validated_data['receive_interesting_offers']
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessmanCreateAPIView(APIView):
    def post(self, request):
        serializer = BusinessmanRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Попытка найти пользователя по email
            user, created = User.objects.get_or_create(
                email=serializer.validated_data['email'],
                defaults={
                    'username': serializer.validated_data['email'],
                    'password': serializer.validated_data['password'],
                }
            )
            # Если пользователь уже существует, возвращаем ошибку
            if not created:
                return Response({'error': 'Пользователь с таким email уже существует'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Создаем бизнесмена, связанного с пользователем
            businessman = Businessman.objects.create(
                user=user,
                interest_sectors=serializer.validated_data['interest_sectors'],
                business_range=serializer.validated_data['business_range'],
                receive_interesting_offers=serializer.validated_data['receive_interesting_offers']
            )
            # Возвращаем успешный ответ
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Возвращаем ошибку, если данные невалидны
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Неправильные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()

class SendEmailVerification(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Генерация JWT токена
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            # Отправка электронного письма с ссылкой для верификации
            send_mail(
                'Подтверждение почты',
                f'Для завершения регистрации перейдите по ссылке: http://45.8.99.132/verify_email?token={token}',
                'fund4pro@schoolprojecttesting.ru',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Email verification link sent'})
        else:
            return Response({'message': 'User not found'}, status=404)