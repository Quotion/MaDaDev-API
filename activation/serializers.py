from main.models import User
from activation import encoding

from rest_framework import serializers

from django.contrib.auth.tokens import default_token_generator


class UidAndTokenSerializer(serializers.Serializer): # noqa
    default_error_messages = {
        "invalid_token": "Invalid token",
        "invalid_uid": "Invalid UID",
        "stale_token": "Token was staled"
    }

    def validate(self, attrs):
        uid = self.initial_data.get("code", "").split("/")[0]
        token = self.initial_data.get("code", "").split("/")[1]

        try:
            id = encoding.decode_uid(uid)
            self.user = User.objects.get(pk=id)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError) as error:
            key_error = "invalid_uid"
            raise serializers.ValidationError({"uid": [self.error_messages[key_error]]}, code=key_error)

        is_token_valid = default_token_generator.check_token(self.user, token)

        if is_token_valid:
            return attrs
        else:
            key_error = "invalid_token"
            raise serializers.ValidationError({"token": [self.error_messages[key_error]]}, code=key_error)


class ActivationEmailSerializer(UidAndTokenSerializer): # noqa
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.user.is_email_verified:
            return attrs
        raise serializers.ValidationError({"status": "error"})

    def get_user(self):
        return self.user


class RecoveryPasswordSerializer(UidAndTokenSerializer): # noqa
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        self.user.set_password(attrs['password'])
        self.user.save()

        return attrs

    def get_user(self):
        return self.user
