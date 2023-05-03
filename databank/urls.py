from django.urls import path
from .views import *

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', NewTokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/add-funds/<int:pk>/', AddFundsView.as_view(), name='add_funds'),
    path('profile/user/', UserView.as_view(), name='user'),
]
