from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Rider, Quote, Order, Invoice
User = get_user_model()

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=32, 
        required=True
        )
    first_name = serializers.CharField(max_length=32, required=False, allow_blank=True, default='')
    last_name = serializers.CharField(max_length=32, required=False, allow_blank=True, default='')
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=False,
        allow_blank=True,
        default=''
    )
    password = serializers.CharField(min_length=8, required=True)
    bio = serializers.CharField(required=False, allow_blank=True, default='')
    location = serializers.CharField(max_length=32, required=False, allow_blank=True, default='')

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'bio', 'location']

class ObtainTokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        user_serializer = UserModelSerializer(self.user)

        user_data = {}
        user_data['success'] = True
        user_data['authentication'] = {}
        user_data['authentication']['access_token'] = str(refresh.access_token)
        user_data['authentication']['refresh_token'] = str(refresh)
        user_data['user'] = {}
        user_data['user'].update(user_serializer.data)

        return user_data

class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = '__all__'
        read_only_fields = ['created_ts', 'updated_ts']


class QuoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    class Meta:
        model = Quote
        fields = '__all__'
        read_only_fields = ['user', 'created_ts', 'updated_ts']


class OrderSerializer(serializers.ModelSerializer):
    rider = RiderSerializer(required=False)
    quote = QuoteSerializer(required=False)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['quote', 'created_ts', 'updated_ts']

class InvoiceSerializer(serializers.ModelSerializer):
    order = OrderSerializer(required=False)
    quote = QuoteSerializer(required=False)
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['quote', 'created_ts', 'updated_ts']
