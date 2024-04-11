from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User


class Authenticate(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_token(self, instance):
        token = RefreshToken.for_user(self.instance).access_token
        return '{}'.format(token)


class UserCreateSerializer(serializers.ModelSerializer):
    """This serializer for site owner registration"""
    token = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,
                                     required=True, validators=[validate_password, ])

    class Meta:
        model = User
        fields = ('id', 'token', 'email', 'phone_number', 'name', 'image', 'password')

    def get_token(self, instance):
        token = RefreshToken.for_user(self.instance).access_token
        return '{}'.format(token)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """This serializer for Owner login"""
    email = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=2, write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        fields = ['email', 'password', 'token']

