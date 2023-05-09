from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token    = serializers.SerializerMethodField()
    profile  = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'token',
                  'profile', 'id')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def get_profile(self, obj):
        profile = Profile.objects.get(user=obj)
        return ProfileSerializer(profile).data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class RentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    bike_id = serializers.PrimaryKeyRelatedField(queryset=Bike.objects.all(), source='bike', write_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all(), source='plan', write_only=True)
    class Meta:
        model = Rent
        fields = ('user_id', 'bike_id', 'plan_id', 'start_date', 'end_date')

    def create(self, validated_data):
            return Rent.objects.create(
                user=validated_data['user_id'],
                bike=validated_data['bike_id'],
                plan=validated_data['plan_id'],
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date')
            )
