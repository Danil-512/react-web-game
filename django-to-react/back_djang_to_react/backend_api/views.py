from django.core.cache import cache

from django.contrib.auth import authenticate, login, logout

# Модели и сериалайзеры для работы с законами и статьями
from .serializer import UserLoginPasswordSerializer

# Модели и сериалайзеры для работы с авторизацией и регистрацией пользователей
from .models import CustomUser, UserInfo

# Отвечает за отправляемые по сети данные
from rest_framework.response import Response

# Импорт моих функций
from .functions_to_auth_and_reg import add_new_user, access_type_create

# Функции для работы с редисом
from .functions_to_redis import check_user_token_in_redis, debug_redis_sessions, test_redis_connection

from django.middleware.csrf import get_token
import requests
from rest_framework.views import APIView
# Импорт для использования стандартных htpp статусов в ответах
from rest_framework import status


base_rest_api_url = 'http://127.0.0.1:7000/rest_api/'

# Функция для цветного вывода в консоль
def color_print(text, color):
    if   color.upper() == 'BLUE':
        print("\033[34m{}".format(text))
    elif color.upper() == 'RED':
        print("\033[31m{}".format(text))
    else:
        print("\033[33m{}".format(text))
    print("\033[0m{}".format(''))

# Получение данных о текущей сессии - проверка авторизации пользователя
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

# Авторизация пользователя
class AuthorizationUser(APIView):
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
        #
        serializer = UserLoginPasswordSerializer(data=request.data)
        #
        # Если полученные данные не соответствуют формату сериалайзера, то фреймворк автоматически вернет ошибку 400 с информацией об ошибке
        serializer.is_valid(raise_exception=True)
        #
        # Получение переменных с логином и паролем из сериалайзера
        v_login    = serializer.validated_data['userLogin']
        v_password = serializer.validated_data['userPassword']
        #
        # Аутентификация - проверка правильности логина и пароля
        user_data  = authenticate(request, username=v_login, password=v_password)
        #
        # Если пользователь имеет право доступа, даем ему доступ
        if user_data is not None:
            # Перед логином
            print(f"\nBEFORE LOGIN: Session exists: {'yes' if hasattr(request, 'session') else 'no'}")
            if hasattr(request, 'session'):
                print(f"Session key before: {request.session.session_key}")
                print(f"Session data before: {dict(request.session)}")

            # Логин и сохранение
            login(request, user_data)
            request.session.modified = True  # Важно!
            request.session.save()

            # После логина
            print(f"\nAFTER LOGIN: Session key: {request.session.session_key}")
            print(f"Session data: {dict(request.session)}")
            print(f"User authenticated: {request.user.is_authenticated}")
            #
            # Проверка записи в Redis
            redis_key = f'django.contrib.sessions.cache.{request.session.session_key}'
            session_data = cache.get(redis_key)
            print(f"Data in Redis: {session_data}")
            #
            #return Response(f"AuthorizationOK-{user_data.access_type.access_type_descr}")
            # Пользователь успешно авторизован
            return Response(
                {
                    "message": "Авторизация успешна",
                    "access_type": user_data.access_type.access_type_descr
                },
                status=status.HTTP_200_OK
            )
        else:
            print(f"Ошибка авторизации!")
            #
            return Response(
                {"error": "Неверный логин или пароль"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class RegisterUser(APIView):
    def post(self, request):
        print('Попытка регистрации пользователя RegisterUser.post')
        #
        serializer = UserLoginPasswordSerializer(data=request.data)
        #
        print(f'request.data is {request.data}')
        #
        # Если полученные данные не соответствуют формату сериалайзера, то фреймворк автоматически вернет ошибку 400 с информацией об ошибке
        serializer.is_valid(raise_exception=True)
        #
        # Получение переменных с логином и паролем из сериалайзера
        v_login = serializer.validated_data['userLogin']
        v_password = serializer.validated_data['userPassword']
        #
        if len(v_password) < 6 or len(v_login) < 6:
            return Response(
                {"error": "Логин и пароль должны быть не менее 6 символов!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        #
        # Попытка регистрации пользователя
        try:
            user_data = CustomUser.objects.create_user(
                username=v_login,
                password=v_password
            )
            #
            UserInfo.objects.create(user=user_data)  # Создаем пустую запись UserInfo
            #
            print(f'Пользователь v_login успешно зарегистрирован ')
            #
            return Response(
                {"message": "Пользователь успешно зарегистрирован!"},
                status=status.HTTP_201_CREATED
            )
        #
        except Exception as e:
            print(f"Ошибка регистрации: {str(e)}")
            #
            return Response(
                {"error": "Не удалось зарегистрировать пользователя"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
            'access_description': user.access_type.access_type_descr,
        }

        return Response(response_data)




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
                f'{base_rest_api_url}laws/{p_law_id}/newArticle/',
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