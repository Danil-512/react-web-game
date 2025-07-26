from django.core.cache import cache

from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
# Модели и сериалайзеры для работы с законами и статьями
from .serializer import MyClass1Serializer

# Модели и сериалайзеры для работы с авторизацией и регистрацией пользователей
from .models import CustomUser, UserInfo

# Отвечает за отправляемые по сети данные
from rest_framework.response import Response

# Импорт моих функций
from .functions_to_auth_and_reg import add_new_user, access_type_create

# Функции для работы с редисом
from .functions_to_redis import check_user_token_in_redis, debug_redis_sessions, test_redis_connection

base_rest_api_url = 'http://127.0.0.1:7000/rest_api'

# Функция для цветного вывода в консоль
def color_print(text, color):
    if   color.upper() == 'BLUE':
        print("\033[34m{}".format(text))
    elif color.upper() == 'RED':
        print("\033[31m{}".format(text))
    else:
        print("\033[33m{}".format(text))
    print("\033[0m{}".format(''))






class CheckSessionView(APIView):
    def get(self, request):
        print("\n=== Session Check ===")
        print("Session Key:", request.session.session_key)
        print("Session Data:", dict(request.session))
        print("User:", request.user)
        print("Authenticated:", request.user.is_authenticated)

        if request.user.is_authenticated:
            return Response({
                'is_authenticated': True,
                'username': request.user.username,
                'session_key': request.session.session_key,
                'session_data': dict(request.session)
            })

        return Response({
            'is_authenticated': False,
            'session_key': request.session.session_key if hasattr(request, 'session') else None,
            'cookies_received': dict(request.COOKIES)
        })


class GetCSRFToken(APIView):
    def get(self, request):
        print('Вызов функции для получения нового токена')
        response = Response()
        origin = request.headers.get('Origin')
        if origin in ["http://localhost:5173", "http://127.0.0.1:5173"]:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
        get_token(request)  # Это установит CSRF cookie
        print(f'Новый токен: {request}')
        return response

class MyClass1View(APIView):
    def options(self, request, *args, **kwargs):
        response = Response()
        origin = request.headers.get('Origin')
        if origin in ["http://localhost:5173", "http://127.0.0.1:5173"]:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
    def get(self, request):
        # Возвращаем пустой ответ, но с правильными CORS заголовками
        response = Response()
        response['Access-Control-Allow-Origin'] = request.headers.get('Origin', 'http://localhost:5173')
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    def post(self, request):
        print("\n=== ИНФОРМАЦИЯ О СЕССИИ ===")
        print(f"Session Key: {request.session.session_key}")
        print(f"Session Data: {dict(request.session)}")
        print(f"User: {request.user}")
        print(f"Authenticated: {request.user.is_authenticated}")
        print(f"Request COOKIES: {request.COOKIES}")
        print("=========================\n")
        print("-----------------------------------------")
        print("Request data:", request.data)
        serializer = MyClass1Serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            v_type = serializer.validated_data['type']
            print(f'Получен запрос типа: {v_type}')

            if v_type == "register":
                v_login = serializer.validated_data['data1']
                v_password = serializer.validated_data['data2']

                if len(v_password) < 6 or len(v_login) < 6:
                    return Response('RegisterNOTOK')

                try:
                    user = CustomUser.objects.create_user(
                        username=v_login,
                        password=v_password
                    )
                    UserInfo.objects.create(user=user)  # Создаем пустую запись UserInfo
                    return Response("RegisterOK")
                except Exception as e:
                    print(f"Ошибка регистрации: {str(e)}")
                    return Response("RegisterNOTOK")


            if v_type == "exit":
                # Изменено: используем стандартный logout Django
                logout(request)
                print("Выход из аккаунта")
                return Response("ExitOK")

            if v_type == "authorization":
                v_login = serializer.validated_data['data1']
                v_password = serializer.validated_data['data2']

                user = authenticate(request, username=v_login, password=v_password)

                if user is not None:
                    # Перед логином
                    print(f"\nBEFORE LOGIN: Session exists: {'yes' if hasattr(request, 'session') else 'no'}")
                    if hasattr(request, 'session'):
                        print(f"Session key before: {request.session.session_key}")
                        print(f"Session data before: {dict(request.session)}")

                    # Логин и сохранение
                    login(request, user)
                    request.session.modified = True  # Важно!
                    request.session.save()

                    # После логина
                    print(f"\nAFTER LOGIN: Session key: {request.session.session_key}")
                    print(f"Session data: {dict(request.session)}")
                    print(f"User authenticated: {request.user.is_authenticated}")

                    # Проверка записи в Redis
                    redis_key = f'django.contrib.sessions.cache.{request.session.session_key}'
                    session_data = cache.get(redis_key)
                    print(f"Data in Redis: {session_data}")

                    return Response(f"AuthorizationOK-{user.access_type.access_type_descr}")


class GetActualUser(APIView):
    def get(self, request):
        print('Запрос от клиента на получение информации об актуальном пользователе')
        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return Response({
                'is_authenticated': False,
                'login': '',
                'access_description': '',
            }, status=401)

        # Получаем текущего пользователя
        user = request.user

        # Формируем ответ с данными пользователя
        response_data = {
            'is_authenticated': True,
            'login': user.username,
            # 'accessLevel': user.access_type.access_type_id,
            'access_description': user.access_type.access_type_descr,
            # 'firstName': user.userinfo.first_name if hasattr(user, 'userinfo') else '',
            # 'lastName': user.userinfo.second_name if hasattr(user, 'userinfo') else '',
            # 'email': user.userinfo.email if hasattr(user, 'userinfo') else ''
        }

        return Response(response_data)

from django.middleware.csrf import get_token
import requests
from rest_framework.views import APIView
from rest_framework.response import Response

class NewArticle(APIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request, p_law_id):
        print("User auth status:", request.user.is_authenticated)
        print("Session auth:", request.session.get('_auth_user_id'))
        print("\n=== NewArticle Debug ===")
        print("User:", request.user)  # Проверка аутентификации
        print("Data:", request.data)  # Проверка данных
        print("Headers:", request.headers)

        csrf_token = request.headers['X-Csrftoken']
        print(f'csrf_token is: {csrf_token}')
        # Информация о пользователе
        print("User:", request.user)
        print("Is authenticated:", request.user.is_authenticated)

        # Информация о сессии
        session = request.session
        print("\nSession info:")
        print("Session key:", session.session_key)
        print("Session data:", dict(session))
        print("Session expiry age:", session.get_expiry_age())
        print("Session expiry date:", session.get_expiry_date())

        # Подготовка данных для второго сервера
        data = {
            'article_title': request.data.get('article_title'),
            'points': request.data.get('points', []),
            'responsibilities': request.data.get('responsibilities', {}),
            'original_user': str(request.user),  # Добавляем информацию о пользователе
            'original_law_id': p_law_id
        }

        try:
            # Отправка на второй сервер
            response = requests.post(
                f'http://127.0.0.1:7000/rest_api/laws/{p_law_id}/newArticle/',
                json=data,  # Автоматически преобразует в JSON и устанавливает Content-Type
                headers={
                    'Content-Type': 'application/json',
                    'X-CSRFToken': request.META.get('CSRF_COOKIE', ''),
                },
                timeout=5  # Таймаут 5 секунд
            )

            print(f"Response from secondary server: {response.status_code} - {response.text}")

            # Проверяем ответ второго сервера
            if response.status_code in [200, 201]:
                return Response('NewArticleOK')
            else:
                return Response('NewArticleOK')

        except requests.exceptions.RequestException as e:
            print(f"Request to secondary server failed: {str(e)}")
            return Response({
                'status': 'error',
                'message': f'Failed to connect to secondary server: {str(e)}'
            }, status=503)