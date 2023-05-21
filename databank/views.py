from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .serializers import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
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
class UpdateProfileView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
        instance = self.get_queryset().get()
        if request.data.get('address') is not '':
            instance.address  = request.data.get('address')
        if request.data.get('zip_code') is not '':
            instance.zip_code = request.data.get('zip_code')
        if request.data.get('location') is not '':
            instance.location = request.data.get('location')
        if request.data.get('phone') is not '':
            instance.phone    = request.data.get('phone')
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class AddFundsView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
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
            instance = self.get_queryset().get()
            # Update the fields as needed
            instance.funds += funds
            instance.save()
            # Return the updated instance
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid card information or funds amount.'})

class BikeListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer

class BikeDetailView(generics.RetrieveAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    lookup_field = 'serie_number'

class PlanListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class RentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Rent.objects.all()
    serializer_class = RentSerializer

    def get_queryset(self):
        user = self.request.user
        return Rent.objects.filter(user=user)

class RentDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Rent.objects.all()
    serializer_class = RentGetSerializer
    lookup_field = 'id'

class RentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RentSerializer
    def perform_create(self, serializer):
        condition = (get_rent.count() == 0)
        if condition:
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError({'error': 'Bike already rented.'})

    def post(self, request, *args, **kwargs):
        plan_id = int(request.data.get('plan_id'))
        try:
            get_plan = Plan.objects.get(id=plan_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'error': 'Invalid plan ID.'})
        get_bike  = Bike.objects.get(serie_number=request.data.get('bike'))
        date_rent = datetime.now() + timedelta(days=get_plan.duration)
        get_rent  = Rent.objects.filter(bike=get_bike, get_plan=get_plan,
                                        start_date__lte=date_rent)
        condition = (get_rent.count() == 0)
        if condition:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)
        else:
            raise serializers.ValidationError({'error': 'Bike already rented.'})
