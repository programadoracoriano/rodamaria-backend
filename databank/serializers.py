from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

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

class PlanCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanCategory
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    category = PlanCategorySerializer(read_only=True)
    class Meta:
        model = Plan
        fields = '__all__'

class RentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Rent
        fields = ('plan', 'bike', 'start_date', 'user')

    def validate(self, attrs):
        plan_id = attrs.get('plan')
        if plan_id is None:
          raise serializers.ValidationError({'error': 'Missing plan_id field.'})
        try:
            get_plan = Plan.objects.get(name=plan_id)
        except Plan.DoesNotExist:
            raise serializers.ValidationError({'error': 'Invalid plan ID.'})

        get_bike = Bike.objects.get(name=str(attrs.get('bike')))
        date_rent = datetime.now() + timedelta(days=get_plan.duration)
        get_rent = Rent.objects.filter(bike=get_bike, plan=get_plan,
                                       start_date__lte=date_rent)
        if get_rent.exists():
            raise serializers.ValidationError({'error': 'Bicicleta já está alugada.'})

        attrs['user'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        plan = validated_data.get('plan')
        user = validated_data.get('user')
        bike = validated_data.get('bike')

        if not plan or not user or not bike:
            raise serializers.ValidationError({'error': 'Tens de escolher um plano.'})
        if user.profile.funds < plan.price:
            raise serializers.ValidationError({'error': 'Saldo insuficiente.'})

        # Subtract funds from user
        user.profile.funds -= plan.price
        user.profile.save()

        return Rent.objects.create(**validated_data)


class RentGetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    bike = BikeSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)
    class Meta:
        model = Rent
        fields = '__all__'

class PlaceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceCategory
        fields = '__all__'

class PlaceSerializer(serializers.ModelSerializer):
    category = PlaceCategorySerializer(read_only=True)
    class Meta:
        model = Place
        fields = '__all__'
