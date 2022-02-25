from django.contrib.auth import login, logout

from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, mixins, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from activation.views import ConfirmEmail, PasswordChangedEmail, PasswordRecoveryEmail, ReConfirmEmail
from main import schemas
from main.schemas import UsersSchemas, AuthUserSchemas, ProductSchemas, ProductTypeSchemas
from main.serializers import *


class UsersViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes_by_action = {'list': [permissions.IsAdminUser | permissions.DjangoModelPermissions],
                                    'create': [permissions.AllowAny],
                                    'delete': [permissions.IsAdminUser | permissions.DjangoModelPermissions]}

    @staticmethod
    def get_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @swagger_auto_schema(tags=["user"],
                         manual_parameters=UsersSchemas.send_list(),
                         responses=UsersSchemas.response_list(),
                         security=[schemas.bearer()],
                         operation_id="list of users")
    def list(self, request, *args, **kwargs):
        """
        Список пользователей
        ===
        При выводе полного списка пользователей можно указать `offset`, а также `limit`, для того чтобы либо сократить
        ваш список, либо сдвинуть его.
        """
        response = super(UsersViewSet, self).list(request, *args, **kwargs)

        if not request.user.has_perm('main.view_user'):
            return Response({"status": "user dont have permissions"}, status=status.HTTP_403_FORBIDDEN)

        return response

    @swagger_auto_schema(tags=["user"],
                         request_body=UsersSchemas.fields_create(),
                         responses=UsersSchemas.response_create(),
                         security=[schemas.basic()],
                         operation_id="register user")
    def create(self, request, *args, **kwargs):
        """
        Регистрация пользователя
        ===
        При использовании данной опции учтите, что у пользователя должны быть **индивидуальными** как `email`,
        так и `username`.\n
        Данный метод защищен от повторной регистрации с одного и того же IP-адреса. Но если же пользователь
        забыл пароль или же не может подтвердить почту, ему необходимо будет обратиться к Администрации.
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

    @swagger_auto_schema(tags=["user"],
                         request_body=UsersSchemas.request_body_id(),
                         manual_parameters=UsersSchemas.manual_request_update(),
                         responses=UsersSchemas.response_list(),
                         security=[schemas.bearer()],
                         operation_id="update user")
    def update(self, request, *args, **kwargs):
        """
        Изменение пользователя
        ===
        В данном случае можно изменить только `username`, `email`, `image` и поля администрации `is_staff` и
        `is_superuser`
        """

        if not request.data:
            return Response({"empty": "request data is empty"}, status.HTTP_400_BAD_REQUEST)

        email = 'email' in request.data.keys()

        instance = self.get_object()

        serializer = UpdateUserSerializer(ip=self.get_ip(request), instance=instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        if email:
            context = {'user': instance}
            to = [instance.email]
            ReConfirmEmail(request, context).send(to)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status.HTTP_200_OK, headers=headers)

    @swagger_auto_schema(tags=["user"],
                         path=UsersSchemas.request_body_id(),
                         responses=UsersSchemas.response_delete(),
                         security=[schemas.bearer()],
                         operation_id="delete user")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthAPIView(viewsets.ViewSet):
    serializer_class = LoginSerializer

    permission_classes_by_action = {'login': [permissions.AllowAny],
                                    'send_mail_recovery_password': [permissions.AllowAny]}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(tags=["auth"],
                         request_body=AuthUserSchemas.login_request(),
                         responses=AuthUserSchemas.response_login(),
                         security=[schemas.basic()],
                         operation_id="login")
    def login(self, request, *args, **kwargs):
        """
        Login пользователя
        ===
        Когда пользователь входит, на выход предоставляется `access_token` и `refresh_token`, которые необходимо
        использовать для определения пользователя, который совершает тот или иной запрос.
        ## Важно ##
        После логина необходимо использовать `access_token` в **headers** с ключевым словом «**Bearer**».
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.get_user()

        login(request, user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(tags=["auth"],
                         responses=AuthUserSchemas.response_logout(),
                         security=[schemas.bearer()],
                         operation_id="logout")
    def logout(self, request, *args, **kwargs):
        """
        Logout пользователя
        ===
        После выхода из аккаунта пользователя, необходимо вернуться к использованию `OAuth Token`, чтобы
        далее использовать все доступные средства API
        """
        logout(request)

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(tags=["auth"],
                         request_body=AuthUserSchemas.change_password_request(),
                         responses=AuthUserSchemas.change_password_response(),
                         security=[schemas.bearer()],
                         operation_id="password change")
    def change_password(self, request, *args, **kwargs):
        """
        Изменения пароля
        ===
        Для изменения пароля нужно отправить на сервер старый и новый пароль. Иначе, необходимо восстановление.
        """

        if not request.user.is_authenticated:
            return Response({"status": "user is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user

        serializer = PasswordChangeSerializer(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            context = {'user': user}
            PasswordChangedEmail(request, context).send(user)

            return Response({'status': "ok"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(tags=["auth"],
                         request_body=AuthUserSchemas.send_email_recovery_request(),
                         responses=AuthUserSchemas.send_email_recovery_response(),
                         security=[schemas.basic()],
                         operation_id="send password recovery token")
    def send_mail_recovery_password(self, request, *args, **kwargs):
        """
        Отправка токена изменения пароля
        ===
        Отправляя токен для восстановления пароля. После того как пользователь получит токен, необходимо
        отправить `token`, полученный по почте, и новый пароль на `activate`, чтобы завершить восстановление.
        ## Важно ##
        1. Без **подтвержденной почты** письмо приходить не будет!
        2. **Валидацию паролей** необходимо проводить на FrontEnd-е!
        3. Необходимо предоставить либо `username`, либо `email`. Оба поля предоставлять не нужно!
        4. Если пользователь повторит **login**, предыдущий токен активации будет недействителен!
        Необходимо повторно выслать токен на email пользователя.
        """
        serializer = PasswordRecoverySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.get_user()

            context = {'user': user}
            PasswordRecoveryEmail(request, context).send(to=user)

            return Response({'status': "email send to user"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(tags=["auth"],
                         responses=AuthUserSchemas.confirm_email_response(),
                         security=[schemas.bearer()],
                         operation_id="email confirm")
    def confirm_email(self, request, *args, **kwargs):
        """
        Повторное подтверждение почты
        ===
        Отправляется токен для повторного подтверждения почты
        """
        if request.user.is_email_verified:
            return Response({"status": "email already verified"}, status=status.HTTP_409_CONFLICT)

        context = {'user': request.user}
        ReConfirmEmail(request, context).send([request.user.email])

        return Response({"status": "email send"}, status.HTTP_200_OK)


class ProductAPIView(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @swagger_auto_schema(tags=["product"],
                         request_body=ProductSchemas.product_request(),
                         responses=ProductSchemas.product_response(),
                         security=[schemas.bearer()],
                         operation_id="create product")
    def create(self, request, *args, **kwargs):
        """
        Создания продукта проекта
        ===
        Продукт проекта - это то что создает MaDaDev Inc.
        """
        response = super(ProductAPIView, self).create(request, *args, **kwargs)
        return response

    @swagger_auto_schema(tags=["product"],
                         manual_parameters=ProductSchemas.send_list(),
                         responses=ProductSchemas.response_list(),
                         operation_id="get list products")
    def list(self, request, *args, **kwargs):
        """
        Список продуктов проекта
        ===
        Продукт проекта - это то что создает MaDaDev Inc.
        """
        response = super(ProductAPIView, self).list(request, *args, **kwargs)
        return response

    @swagger_auto_schema(tags=["product"],
                         responses=ProductSchemas.response_delete(),
                         security=[schemas.bearer()],
                         operation_id="delete product")
    def destroy(self, request, *args, **kwargs):
        """
        Удаление продукта проекта
        ===
        Продукт проекта - это то что создает MaDaDev Inc.
        """
        response = super(ProductAPIView, self).list(request, *args, **kwargs)
        return response


class ProductTypeAPIView(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = ProductTypeSerializer
    queryset = TypeProduct.objects.all()

    @swagger_auto_schema(tags=["product"],
                         request_body=ProductTypeSchemas.product_request(),
                         responses=ProductTypeSchemas.product_response(),
                         security=[schemas.bearer()],
                         operation_id="create product type")
    def create(self, request, *args, **kwargs):
        """
        Создания категории продукта проекта
        ===
        """
        response = super(ProductTypeAPIView, self).create(request, *args, **kwargs)
        return response

    @swagger_auto_schema(tags=["product"],
                         manual_parameters=ProductTypeSchemas.send_list(),
                         responses=ProductTypeSchemas.response_list(),
                         operation_id="get list product types")
    def list(self, request, *args, **kwargs):
        """
        Список категорий продуктов проекта
        ===
        """
        response = super(ProductTypeAPIView, self).list(request, *args, **kwargs)
        return response

    @swagger_auto_schema(tags=["product"],
                         responses=ProductTypeSchemas.response_delete(),
                         security=[schemas.bearer()],
                         operation_id="delete product type")
    def destroy(self, request, *args, **kwargs):
        """
        Удаление категории продукта проекта
        ===
        """
        response = super(ProductTypeAPIView, self).list(request, *args, **kwargs)
        return response
