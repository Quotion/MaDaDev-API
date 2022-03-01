from drf_yasg import openapi

from rest_framework import status, serializers


def bearer() -> dict:
    return {"Bearer": []}


def basic() -> dict:
    return {"Basic": []}


def get_status_unauthorized():
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING, description="Запрос не авторизирован или не "
                                                                           "предоставлен токен авторизации")
        }
    )


def get_status_forbidden():
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING, description="Нету прав на выполнения данной операции")
        }
    )


class UsersSchemas:
    @staticmethod
    def request_retrieve_user_id():
        return openapi.Parameter(
            'id',
            openapi.IN_QUERY,
            type=openapi.TYPE_OBJECT,
            description="Первичный ключ пользователя"
        )

    @staticmethod
    def response_user_retrieve():
        return {
            status.HTTP_200_OK: openapi.Schema(
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
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
        }

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
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
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
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
        }

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

    @staticmethod
    def response_delete():
        return {
            status.HTTP_204_NO_CONTENT: openapi.Schema(
                title='answer',
                type=openapi.TYPE_STRING,
                description="Пользователь успешно удален"
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
        }


class AuthUserSchemas:
    @staticmethod
    def login_request():
        return [
            openapi.Parameter(
                'username',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Уникальный логин пользователя"),
            openapi.Parameter(
                'password',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Пароль пользователя")
            ]

    @staticmethod
    def response_login():
        return {
            status.HTTP_200_OK: openapi.Schema(
                title='answer',
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID пользователя"),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description="Логин пользователя"),
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING,
                                                   description="Токен для идентификации пользователя"),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Подтверждена ли почта")
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                title='credentials',
                type=openapi.TYPE_STRING,
                description="Введен не правильный логин или пароль"
            )
        }

    @staticmethod
    def response_logout():
        return {
            status.HTTP_204_NO_CONTENT: openapi.Schema(
                title='answer',
                type=openapi.TYPE_STRING,
                description="Пользователь успешно «разлогинен»"
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized()
        }

    @staticmethod
    def change_password_request():
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['old_password', 'new_password'],
            properties={
                'old_password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Старый пароль"),
                'new_password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Новый пароль")
            })

    @staticmethod
    def change_password_response():
        return {
            status.HTTP_204_NO_CONTENT: openapi.Schema(
                title='answer',
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description="Код ответа")
                },
                description="Пароль изменен"
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                title='bad request',
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description="Код ответа")
                }
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized()
        }

    @staticmethod
    def send_email_recovery_request():
        return [
            openapi.Parameter(
                'username',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Уникальный логин пользователя"),
            openapi.Parameter(
                'email',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Почта пользователя")
        ]

    @staticmethod
    def send_email_recovery_response():
        return {
            status.HTTP_204_NO_CONTENT: openapi.TYPE_STRING,
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                title='bad request',
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description="Код ответа")
                }
            )
        }

    @staticmethod
    def confirm_email_response():
        return {
            status.HTTP_200_OK: openapi.Schema(
                title='Email send',
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description="Письмо отправлено")
                },
            ),
            status.HTTP_409_CONFLICT: openapi.Schema(
                title='Email is verified',
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING,
                                             description="Почта пользователя уже подтверждена")
                }
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized()
        }


class ProductSchemas:
    @staticmethod
    def product_request():
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_title': openapi.Schema(
                    type=openapi.TYPE_STRING),
                'product_tags': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Тэг продукта"),
                'product_desc': openapi.Schema(
                    type=openapi.TYPE_STRING),
                'product_image': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description="Изображение данного продукта"),
                'product_type_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID типа продукта под который он попадает")
            },
            required=['product_title', 'product_tags', 'product_desc', 'product_image', 'product_type_id'])

    @staticmethod
    def product_response():
        return {
            status.HTTP_200_OK: openapi.Schema(
                title='Product type create',
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description="Категория продукта создана")
                },
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
        }

    @staticmethod
    def send_list():
        return [
            openapi.Parameter('limit',
                              openapi.IN_QUERY,
                              description="Лимит по количеству продуктов проекта",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('offset',
                              openapi.IN_QUERY,
                              description="Сдвиг на число продуктов проекта",
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
                        description="Массив содержащий объект в виде полей продуктов проекта",
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT, properties={
                                'product_title': openapi.Schema(type=openapi.TYPE_STRING),
                                'product_tag': openapi.Schema(type=openapi.TYPE_STRING,
                                                              description="Подзаголовочная надпись"),
                                'product_desc': openapi.Schema(type=openapi.TYPE_STRING,
                                                               description="Описание продукта проекта"),
                                'product_image': openapi.Schema(type=openapi.TYPE_STRING,
                                                                description="URI к аватару пользователя"),
                                'product_type_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                                  description="IP при регистрации"),
                            })
                    )}
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
        }

    @staticmethod
    def response_delete():
        return {
            status.HTTP_204_NO_CONTENT: openapi.TYPE_STRING,
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
        }


class ProductTypeSchemas:
    @staticmethod
    def product_request():
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_type_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Название типа продукта")
            },
            required=['product_type_name'])

    @staticmethod
    def product_response():
        return {
            status.HTTP_200_OK: openapi.Schema(
                title='Product type create',
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description="Категория продукта создана")
                },
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
        }

    @staticmethod
    def send_list():
        return [
            openapi.Parameter('limit',
                              openapi.IN_QUERY,
                              description="Лимит по количеству категорий продуктов проекта",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('offset',
                              openapi.IN_QUERY,
                              description="Сдвиг на число категорий продуктов проекта",
                              type=openapi.TYPE_INTEGER)
        ]

    @staticmethod
    def response_list():
        return {
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER,
                                            description="Количество выданных категорий продуктов в поле `results`"),
                    'next': openapi.Schema(type=openapi.TYPE_INTEGER,
                                           description="Номер следующий страницы с данными"),
                    'previous': openapi.Schema(type=openapi.TYPE_INTEGER,
                                               description="Номер предыдущей страницы с данными"),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        description="Массив содержащий объект в виде полей категорий продуктов проекта",
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT, properties={
                                'product_type_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'product_type_name': openapi.Schema(type=openapi.TYPE_STRING),
                            })
                    )}
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
        }

    @staticmethod
    def response_delete():
        return {
            status.HTTP_204_NO_CONTENT: openapi.TYPE_STRING,
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Не правильно введен ID"
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
        }


class MiniNewsSchemas:
    @staticmethod
    def mini_news_request():
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mn_title': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Заголовок новости"),
                'mn_desc': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Описание новости"),
            },
            required=['mn_title', 'mn_desc'])

    @staticmethod
    def mini_news_response():
        return {
            status.HTTP_200_OK: openapi.Schema(
                title='Mini news create',
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description="Мини новость создана")
                },
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
        }

    @staticmethod
    def send_list_mini_news():
        return [
            openapi.Parameter('limit',
                              openapi.IN_QUERY,
                              description="Лимит по количеству мини новостей",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('offset',
                              openapi.IN_QUERY,
                              description="Сдвиг на число мини новостей",
                              type=openapi.TYPE_INTEGER)
        ]

    @staticmethod
    def response_list():
        return {
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER,
                                            description="Количество выданных мини новостей в поле `results`"),
                    'next': openapi.Schema(type=openapi.TYPE_INTEGER,
                                           description="Номер следующий страницы с данными"),
                    'previous': openapi.Schema(type=openapi.TYPE_INTEGER,
                                               description="Номер предыдущей страницы с данными"),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        description="Массив содержащий объект в виде полей мини новостей",
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT, properties={
                                'mini_news_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'mn_title': openapi.Schema(type=openapi.TYPE_STRING),
                                'mn_desc': openapi.Schema(type=openapi.TYPE_STRING),
                                'mn_date': openapi.Schema(type=openapi.TYPE_STRING),
                            })
                    )}
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
        }

    @staticmethod
    def response_delete():
        return {
            status.HTTP_204_NO_CONTENT: openapi.TYPE_STRING,
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Не правильно введен ID"
            ),
            status.HTTP_401_UNAUTHORIZED: get_status_unauthorized(),
            status.HTTP_403_FORBIDDEN: get_status_forbidden()
        }
