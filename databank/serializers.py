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

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class RentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Rent
        fields = ('plan', 'bike', 'start_date', 'user')
    def validate(self, attrs):
        plan_id = attrs.get('plan_id')
        if plan_id is None:
          raise serializers.ValidationError({'error': 'Missing plan_id field.'})
        if not isinstance(plan_id, int):
          raise serializers.ValidationError({'error': 'Invalid plan_id value.'})
        try:
            get_plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            raise serializers.ValidationError({'error': 'Invalid plan ID.'})

        get_bike = Bike.objects.get(serie_number=attrs.get('bike'))
        date_rent = datetime.now() + timedelta(days=get_plan.duration)
        get_rent = Rent.objects.filter(bike=get_bike, plan=get_plan, start_date__lte=date_rent)
        if get_rent.exists():
            raise serializers.ValidationError({'error': 'Bike already rented.'})

        attrs['user'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        plan = validated_data.get('plan')
        user = validated_data.get('user')
        bike = validated_data.get('bike')

        if not plan or not user or not bike:
            raise serializers.ValidationError({'error': 'Incomplete data.'})
        return Rent.objects.create(**validated_data)


class RentGetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    bike = BikeSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)
    class Meta:
        model = Rent
        fields = '__all__'
