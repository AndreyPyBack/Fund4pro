from rest_framework_simplejwt.tokens import RefreshToken
from .models import Businessman
from .serializers import UserLoginSerializer, BusinessmanRegistrationSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import InterestSector, Investor
from .serializers import InterestSectorSerializer, InvestorRegistrationSerializer


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
            # Возвращаем успешный ответ
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Возвращаем ошибку, если данные невалидны
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

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Аутентификация пользователя
            user = authenticate(email=email, password=password)

            # Проверяем, удалось ли аутентифицировать пользователя
            if user is not None:
                # Создаем JWT токены
                refresh = RefreshToken.for_user(user)

                # Возвращаем токены в ответе
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                # Если пользователь не найден или пароль неверный, возвращаем ошибку
                return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Если входные данные недопустимы, возвращаем ошибку
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)