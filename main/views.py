from django.contrib.auth import login, logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from activation.views import ConfirmEmail
from main.schemas import *
from main.serializers import *


class UsersViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    @staticmethod
    def get_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip

    @swagger_auto_schema(manual_parameters=UsersSchemas.send_list(), responses=UsersSchemas.response_list())
    def list(self, request, *args, **kwargs):
        """
        Список пользователей
        ===
        При выводе полного списка пользователей можно указать `offset`, а также `limit`, для того чтобы либо сократить
        ваш список, либо сдвинуть его.
        """
        response = super(UsersViewSet, self).list(request, *args, **kwargs)
        return response

    @swagger_auto_schema(request_body=UsersSchemas.fields_create(), responses=UsersSchemas.response_create())
    def create(self, request, *args, **kwargs):
        """
        Создание пользователя
        ===
        При использовании данного параметра учтите, что у пользователя должны быть **индивидуальными** как `email`,
        так и `username`.
        """
        serializer = self.serializer_class(data=request.data, ip=self.get_ip(request))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = User.objects.get(username=request.data.get('username'))

        context = {'user': user}
        to = [user.email]
        ConfirmEmail(request, context).send(to)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(request_body=UsersSchemas.request_body_update(),
                         manual_parameters=UsersSchemas.manual_request_update(),
                         responses=UsersSchemas.response_list())
    def update(self, request, *args, **kwargs):
        """
        Изменение пользователя
        ===
        В данном случае можно изменить только `username`, `email`, `image` и поля администрации `is_staff` и
        `is_superuser`
        """
        if len(request.data) == 1 and 'access_token' in request.data.keys():
            return Response({"empty": "request is empty"}, status.HTTP_400_BAD_REQUEST)

        email = 'email' in request.data.keys()

        instance = self.get_object()

        serializer = UpdateUserSerializer(ip=self.get_ip(request), instance=instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        if email:
            context = {'user': instance}
            to = [instance.email]
            ConfirmEmail(request, context).send(to)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status.HTTP_200_OK, headers=headers)


class AuthAPIView(viewsets.ViewSet):
    serializer_class = LoginSerializer

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.get_user()

        login(request, user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        logout(request)

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk, *args, **kwargs):
        print(pk)
        print(request.POST)
        return Response({'status': "ok"})

    @action(detail=True, methods=['post'])
    def confirm_email(self, request, host, *args, **kwargs):
        pass
