from django.urls import path
from .views import InterestSectorListCreateAPIView, InvestorCreateAPIView

urlpatterns = [
    path('api/interest-sectors/', InterestSectorListCreateAPIView.as_view(), name='interest-sectors'),
    path('api/register/investor/', InvestorCreateAPIView.as_view(), name='register-investor'),
]
