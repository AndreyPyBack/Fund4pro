from django.urls import path
from .views import UserLoginView, InterestSectorListCreateAPIView, InvestorCreateAPIView, BusinessmanCreateAPIView, \
    SendEmailVerification

urlpatterns = [
    path('api/interest-sectors/', InterestSectorListCreateAPIView.as_view(), name='interest-sectors'),
    path('api/register/investor/', InvestorCreateAPIView.as_view(), name='register-investor'),
    path('api/register/businessman/', BusinessmanCreateAPIView.as_view(), name='businessman-register'),
    path('api/login/', UserLoginView.as_view(), name='users-login'),
    path('api/confirm_email/', SendEmailVerification.as_view(), name='user-confirm'),
]
