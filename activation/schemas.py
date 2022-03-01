from drf_yasg import openapi

from rest_framework import status


class TokensSchemas:
    @staticmethod
    def token_request():
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(type=openapi.TYPE_STRING,
                                       description="Токен/код активации"),
                'status': openapi.Schema(type=openapi.TYPE_STRING,
                                         enum=["confirm", "recovery"],
                                         description="`confirm`: подтверждение почты "
                                                     "`recovery`: восстановление пароля")
            },
            required=['code', 'status']
        )

    @staticmethod
    def token_response():
        return {
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description="Возвращает статус токена")
                }
            )
        }
