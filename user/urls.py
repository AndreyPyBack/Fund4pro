from django.urls import path
from .views import InvestorCreateView, BusinessmanCreateView, UserLoginView

urlpatterns = [
    path('api/investor/register/', InvestorCreateView.as_view(), name='investor-register'),
    path('api/businessman/register/', BusinessmanCreateView.as_view(), name='businessman-register'),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
]
