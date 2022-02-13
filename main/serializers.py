from main.models import User
from MaDaDevAPI import settings

from rest_framework import serializers

from django.contrib.auth import authenticate
from django.db import models

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    image = serializers.ImageField(max_length=255)
    email = serializers.EmailField(max_length=128)

    def __init__(self, ip=None, *args, **kwargs):
        super(CreateUserSerializer, self).__init__(*args, **kwargs)
        self.ip = ip

    def create(self, validated_data):
        image = validated_data.get('image')

        if image:
            if settings.IMAGE_LIMIT_SIZE * 1024 * 1024 < image.size:
                raise serializers.ValidationError(f'Size of image more then {settings.IMAGE_LIMIT_SIZE}MB',
                                                  code='big_image')

        try:
            User.objects.get(username=validated_data.get('username'))
            User.objects.get(email=validated_data.get('email'))
        except models.ObjectDoesNotExist:
            pass
        else:
            raise serializers.ValidationError('User with this username or email already exist',
                                              code='username_or_email_exist')

        user = User.objects.create_user(username=validated_data.get('username'),
                                        email=validated_data.get('email'),
                                        image=validated_data.get('image'),
                                        password=validated_data.get('password'))

        if self.ip:
            user.ip = self.ip

        user.save()

        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_email_verified', 'image', 'ip', 'last_ip',
                  'is_staff', 'is_superuser', 'date_joined', 'last_login']


class UpdateUserSerializer(serializers.Serializer): # noqa
    username = serializers.CharField(max_length=255, required=False)
    image = serializers.ImageField(required=False)
    is_staff = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)

    def __init__(self, ip=None, *args, **kwargs):
        super(UpdateUserSerializer, self).__init__(*args, **kwargs)
        self.ip = ip

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == "image":
                if settings.IMAGE_LIMIT_SIZE * 1024 * 1024 < value.size:
                    raise serializers.ValidationError(f'Size of image more then {settings.IMAGE_LIMIT_SIZE}MB',
                                                      code='big_image')

                instance.image.storage.delete(instance.image.path)

            elif attr == 'username':
                try:
                    user = User.objects.get(username=value)
                except models.ObjectDoesNotExist:
                    pass
                else:
                    if user != instance:
                        raise serializers.ValidationError('User with this username already exist',
                                                          code='username_exist')

            elif attr == 'email':
                try:
                    user = User.objects.get(email=value)
                except models.ObjectDoesNotExist:
                    pass
                else:
                    if user != instance:
                        raise serializers.ValidationError('User with this username or email already exist',
                                                          code='username_or_email_exist')

            elif attr == 'is_superuser' or attr == 'is_staff':
                pass

            else:
                raise serializers.ValidationError('You cannot change the password fields, registration and '
                                                  'login dates, ip-addresses and another.', code="forbidden_fields")

            setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['username', 'email', 'image', 'is_staff', 'is_superuser']


class LoginSerializer(serializers.Serializer): # noqa
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    user = None

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        self.user = authenticate(username=username, password=password)

        if not self.user:
            raise serializers.ValidationError('A user with this username and password was not found.')

        elif not self.user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        access_token = AccessToken.for_user(self.user)
        refresh_token = RefreshToken.for_user(self.user)

        return {
                'username': self.user.username,
                'access_token': access_token,
                'refresh_token': refresh_token
            }

    def get_user(self):
        return self.user

    class Meta:
        model = User
