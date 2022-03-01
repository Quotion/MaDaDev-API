from main.models import User, Product, TypeProduct, MiniNews
from MaDaDevAPI import settings

from rest_framework import serializers

from django.contrib.auth import authenticate
from django.db import models

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class CreateUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
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
                raise serializers.ValidationError({"status": f'Size of image more then {settings.IMAGE_LIMIT_SIZE}MB'},
                                                  code='big_image')

        try:
            user = User.objects.get(models.Q(username=validated_data.get('username')) |
                                    models.Q(email=validated_data.get('email')) |
                                    models.Q(ip=self.ip) | models.Q(last_ip=self.ip))
        except models.ObjectDoesNotExist:
            pass
        else:
            if user.username == validated_data.get('username'):
                key = "username"
                param = user.username
                status = "username is taken"
            elif user.email == validated_data.get('email'):
                key = "email"
                param = user.username
                status = "email is taken"
            elif user.ip == self.ip or user.last_ip == self.ip:
                key = "ip"
                param = self.ip
                status = "registration with an ip that already exists"

            raise serializers.ValidationError({"status": status,
                                               "user": {key: param}},
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
        fields = ['id', 'username', 'password', 'email', 'is_email_verified', 'image', 'ip', 'last_ip',
                  'is_staff', 'is_superuser', 'date_joined', 'last_login']


class UpdateUserSerializer(serializers.Serializer):  # noqa
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
                    raise serializers.ValidationError({"status": f"Size of image more "
                                                                 f"then {settings.IMAGE_LIMIT_SIZE}MB"},
                                                      code='big_image')

                instance.image.storage.delete(instance.image.path)

            elif attr == 'username':
                try:
                    user = User.objects.get(username=value)
                except models.ObjectDoesNotExist:
                    pass
                else:
                    if user != instance:
                        raise serializers.ValidationError({"status": 'User with this username already exist'},
                                                          code='username_exist')

            elif attr == 'email':
                try:
                    user = User.objects.get(email=value)
                except models.ObjectDoesNotExist:
                    instance.is_email_verified = False
                else:
                    if user != instance:
                        raise serializers.ValidationError({"status": 'User with this email already exist'},
                                                          code='username_or_email_exist')

            elif attr == 'is_superuser' or attr == 'is_staff':
                pass

            else:
                raise serializers.ValidationError({"status": 'You cannot change the password fields, registration and '
                                                             'login dates, ip-addresses and another.'},
                                                  code="forbidden_fields")

            setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['username', 'email', 'image', 'is_staff', 'is_superuser']


class LoginSerializer(serializers.Serializer):  # noqa
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    user = None

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if password is None:
            raise serializers.ValidationError({"status": 'A password is required to log in.'}, code="password_empty")

        self.user = authenticate(username=username, password=password)

        if not self.user:
            raise serializers.ValidationError({"status": 'A user with this username and password was not found.'},
                                              code="user_not_found")

        elif not self.user.is_active:
            raise serializers.ValidationError({"status": 'This user has been deactivated.'},
                                              code="user_not_active")

        access_token = AccessToken.for_user(self.user)
        refresh_token = RefreshToken.for_user(self.user)

        return {
            'id': self.user.id,
            'username': self.user.username,
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def get_user(self):
        return self.user

    class Meta:
        model = User


class PasswordChangeSerializer(serializers.Serializer):  # noqa
    old_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        old_password = data.get('old_password', None)
        new_password = data.get('new_password', None)

        if old_password == new_password:
            raise serializers.ValidationError({"status": "old and new passwords is equal"},
                                              code="invalid_old_new_password")

        if self.instance.check_password(old_password):
            self.instance.set_password(new_password)
            self.instance.save()
        else:
            raise serializers.ValidationError({"status": "invalid old password"}, code="invalid_old_password")

        return {"status": "ok"}


class PasswordRecoverySerializer(serializers.Serializer):  # noqa
    username = serializers.CharField(max_length=255, required=False)
    email = serializers.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super(PasswordRecoverySerializer, self).__init__(self, *args, **kwargs)

        self.user = None

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)

        if not username and not email:
            raise serializers.ValidationError({"status": "username and email is empty"}, code="no_data_entered")

        if username:
            try:
                user = User.objects.get(username=username)
            except models.ObjectDoesNotExist:
                raise serializers.ValidationError({"status": "username not found"}, code="invalid_username")
            else:
                if user.is_email_verified:
                    self.user = user
                    return True
                else:
                    raise serializers.ValidationError({"status": "email not verified"}, code="verified_error")
        else:
            try:
                user = User.objects.get(email=email)
            except models.ObjectDoesNotExist:
                raise serializers.ValidationError({"status": "email not found"}, code="invalid_email")
            else:
                if user.is_email_verified:
                    self.user = user
                    return True
                else:
                    raise serializers.ValidationError({"status": "email not verified"}, code="verified_error")

    def get_user(self):
        return self.user


class ProductSerializer(serializers.Serializer):  # noqa
    product_id = serializers.IntegerField(read_only=True)
    product_title = serializers.CharField(max_length=128)
    product_tag = serializers.CharField(max_length=64)
    product_desc = serializers.CharField()
    product_image = serializers.ImageField()
    product_type_id = serializers.IntegerField()

    def validate(self, data):
        product_type_id = data.get("product_type_id", None)
        try:
            type_product = TypeProduct.objects.get(product_type_id=product_type_id)
        except models.ObjectDoesNotExist:
            raise serializers.ValidationError({"status": "Type product ID not exists"})
        else:
            return True

    class Meta:
        model = Product
        fields = ['product_id', 'product_title', 'product_tag', 'product_desc', 'product_desc', 'product_type_id']


class ProductTypeSerializer(serializers.Serializer):  # noqa
    product_type_id = serializers.IntegerField(read_only=True)
    product_type_name = serializers.CharField(max_length=128)

    class Meta:
        model = TypeProduct
        fields = ['product_type_id', 'product_type_name']


class MiniNewsSerializer(serializers.Serializer):  # noqa
    mini_news_id = serializers.IntegerField(read_only=True)
    mn_title = serializers.CharField(max_length=128)
    mn_desc = serializers.CharField(max_length=128)
    mn_date = serializers.DateField()

    class Meta:
        model = MiniNews
        fields = ['mini_news_id', 'mn_title', 'mn_desc', 'mn_date']
