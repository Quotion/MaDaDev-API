from drf_yasg import openapi

from rest_framework import status


class UsersSchemas:
    @staticmethod
    def send_list():
        return [
            openapi.Parameter('limit',
                              openapi.IN_QUERY,
                              description="Лимит по количеству пользователей",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('offset',
                              openapi.IN_QUERY,
                              description="Сдвиг на число пользователей",
                              type=openapi.TYPE_INTEGER)
        ]

    @staticmethod
    def response_list():
        return {
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER,
                                            description="Количество выданных пользователей в поле `results`"),
                    'next': openapi.Schema(type=openapi.TYPE_INTEGER,
                                           description="Номер следующий страницы с данными"),
                    'previous': openapi.Schema(type=openapi.TYPE_INTEGER,
                                               description="Номер предыдущей страницы с данными"),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        description="Массив содержащий объект в виде полей пользователя",
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT, properties={
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'is_email_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                                    description="Подтверждена ли почта"),
                                'image': openapi.Schema(type=openapi.TYPE_STRING,
                                                        description="URI к аватару пользователя"),
                                'ip': openapi.Schema(type=openapi.TYPE_STRING,
                                                     description="IP при регистрации"),
                                'last_ip': openapi.Schema(type=openapi.TYPE_STRING),
                                'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                           description="Относится ли пользователь к администрации"),
                                'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                               description="Суперадмин ли пользователь"),
                                'date_joined': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_login': openapi.Schema(type=openapi.TYPE_STRING),
                            })
                    )}
            )
        }

    @staticmethod
    def fields_create():
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING,
                                           description="Уникальное имя пользователя"),
                'password': openapi.Schema(type=openapi.TYPE_STRING,
                                           description="Пароль для данного пользователя"),
                'email': openapi.Schema(type=openapi.TYPE_STRING,
                                        description="Почта, на которую придёт токен для активации"),
                'image': openapi.Schema(type=openapi.TYPE_STRING,
                                        description="Аватарка пользователя")
            },
            required=['username', 'password', 'email']
        )

    @staticmethod
    def response_create():
        return {
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'is_email_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                        description="Подтверждена ли почта"),
                    'image': openapi.Schema(type=openapi.TYPE_STRING,
                                            description="URI к аватару пользователя"),
                    'ip': openapi.Schema(type=openapi.TYPE_STRING,
                                         description="IP при регистрации"),
                    'last_ip': openapi.Schema(type=openapi.TYPE_STRING),
                    'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                               description="Относится ли пользователь к администрации"),
                    'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                   description="Суперадмин ли пользователь"),
                    'date_joined': openapi.Schema(type=openapi.TYPE_STRING),
                    'last_login': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }

    @staticmethod
    def request_body_update():
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(
                    openapi.IN_PATH,
                    type=openapi.TYPE_INTEGER,
                    description="Первичный ключ пользователя, которому необходимо изменить данные")
            })

    @staticmethod
    def manual_request_update():
        return [
            openapi.Parameter(
                'username',
                openapi.IN_QUERY,
                description="Уникальное имя пользователя",
                type=openapi.TYPE_STRING),
            openapi.Parameter(
                'email',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING),
            openapi.Parameter(
                'image',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING),
            openapi.Parameter(
                'is_staff',
                openapi.IN_QUERY,
                description="Является ли пользователь частью администрации",
                type=openapi.TYPE_STRING),
            openapi.Parameter(
                'is_superuser',
                openapi.IN_QUERY,
                description="Является ли пользователь суперпользователем, который имеет доступ ко всему",
                type=openapi.TYPE_STRING),
        ]
