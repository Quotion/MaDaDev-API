from main.models import User
from activation import encoding, schemas
from activation.serializers import *

from django.contrib.auth.tokens import default_token_generator

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from templated_mail.mail import BaseEmailMessage

from drf_yasg.utils import swagger_auto_schema


class ConfirmEmail(BaseEmailMessage):
    template_name = "email/activate_email.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["code"] = f"{encoding.encode_uid(user.pk)}/{default_token_generator.make_token(user)}"
        return context


class ReConfirmEmail(BaseEmailMessage):
    template_name = "email/reactivate_email.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["code"] = f"{encoding.encode_uid(user.pk)}/{default_token_generator.make_token(user)}"
        return context


class PasswordChangedEmail(BaseEmailMessage):
    template_name = "email/password_change_email.html"

    def send(self, to, *args, **kwargs):
        if to.is_email_verified:
            super(PasswordChangedEmail, self).send([to.email], *args, **kwargs)
        else:
            return None


class PasswordRecoveryEmail(BaseEmailMessage):
    template_name = "email/recovery_password_email.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["code"] = f"{encoding.encode_uid(user.pk)}/{default_token_generator.make_token(user)}"
        return context

    def send(self, to, *args, **kwargs):
        print(to)
        if to.is_email_verified:
            super(PasswordRecoveryEmail, self).send([to.email], *args, **kwargs)
        else:
            return None


class TokenConfirmView(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    @swagger_auto_schema(tags=['token'],
                         request_body=schemas.TokensSchemas().token_request(),
                         responses=schemas.TokensSchemas().token_response(),
                         operation_id="Check token")
    def activate(self, request):
        """
        Проверка токена
        ===
        Чтобы проверить, что это действительно пользователь хочет изменить пароль, почту или только вписал почту
        проходя по ссылки, вводя токен, он проверятся и возвращается ответ, правда ли это он или кто-то иной.
        """
        status_request = request.POST.get('status')

        if status_request == 'confirm':
            serializer = ActivationEmailSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)

            user = serializer.get_user()
            user.is_email_verified = True
            user.save()

            return Response({"status": "verified"}, status=status.HTTP_200_OK)

        elif status_request == 'recovery':
            serializer = RecoveryPasswordSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)

            return Response({"status": "password reset"}, status=status.HTTP_200_OK)

        else:
            return Response({"status": "status not found"}, status=status.HTTP_400_BAD_REQUEST)

