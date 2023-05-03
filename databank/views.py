from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .serializers import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
class NewTokenRefreshView(TokenRefreshView):
    pass

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = UserSerializer

    def get_object(self):
        return self.request.user

class ProfileView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

class AddFundsView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ProfileSerializer

    def get_object(self):
        return Profile.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        cc_number       = '4242424242424242'
        cc_date_month   = '12'
        cc_date_year    = '2024'
        cc_cvc          = '123'
        card_number     = request.data.get('card_number')
        card_date_month = request.data.get('card_date_month')
        card_date_year  = request.data.get('card_date_year')
        card_cvc        = request.data.get('card_cvc')
        funds           = float(request.data.get('funds'))
        condition = ((card_number == cc_number and card_date_month == cc_date_month
                     and card_date_year == cc_date_year and card_cvc == cc_cvc) and
                     funds > 0 and funds is not None)
        if condition:
            # Get the object to update
            instance = self.get_object()
            # Update the fields as needed
            instance.funds += funds
            instance.save()
            # Return the updated instance
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid card information or funds amount.'})
