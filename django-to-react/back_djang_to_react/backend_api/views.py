import os
from django.conf import settings
from django.http import FileResponse, HttpResponseBadRequest

from django.core.cache import cache
from django.http import JsonResponse
import json

from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.sessions.models import Session

from os import error
from rest_framework.views import APIView
from django.db.models import Max
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from .serializer import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth.hashers import check_password

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password

# Модели и сериалайзеры для работы с законами и статьями
from .models import MyClass1, Laws, Articles, ArticleClauses, RespToArticles #, UsersAccess
from .serializer import MyClass1Serializer, LawsSerializer, ArticlesSerializer, LawsShortSerializer, ArticlesShortSerializer, ArticleClausesSerializer, RespToArticlesSerializer

# Модели и сериалайзеры для работы с авторизацией и регистрацией пользователей
from .models import CustomUserManager, CustomUser, UserInfo, AccessTypes
from .serializer import UsersListSerializer, UsersInfoSerializer

# Отвечает за отправляемые по сети данные
from rest_framework.response import Response

# Импорт моих функций
from .functions_to_auth_and_reg import add_new_user, access_type_create

# Функция для цветного вывода в консоль
def color_print(text, color):
    if   color.upper() == 'BLUE':
        print("\033[34m{}".format(text))
    elif color.upper() == 'RED':
        print("\033[31m{}".format(text))
    else:
        print("\033[33m{}".format(text))
    print("\033[0m{}".format(''))


def debug_redis_sessions(request):
    """Расширенная версия с логированием процесса"""
    try:
        # Логирование текущего состояния
        print("\n=== DEBUG SESSION INFO ===")
        print(f"Current session key: {request.session.session_key}")
        print(f"Session exists in request: {'yes' if hasattr(request, 'session') else 'no'}")

        # Получаем все ключи
        all_keys = cache.keys('*')
        print(f"\nAll keys in Redis: {all_keys}")

        # Фильтруем только сессии
        session_keys = [k for k in all_keys if k.startswith('django.contrib.sessions.cache.')]
        print(f"\nFound {len(session_keys)} session keys")

        sessions = []
        for key in session_keys:
            data = cache.get(key)
            print(f"\nProcessing key: {key}")
            print(f"Raw data: {data}")

            try:
                if isinstance(data, bytes):
                    data = data.decode('utf-8')
                if isinstance(data, str):
                    try:
                        data = json.loads(data)
                    except json.JSONDecodeError:
                        pass

                session_key = key.replace('django.contrib.sessions.cache.', '')
                sessions.append({
                    'key': session_key,
                    'user_id': data.get('_auth_user_id') if isinstance(data, dict) else None,
                    'data': data
                })
            except Exception as e:
                print(f"Error processing key {key}: {str(e)}")
                sessions.append({
                    'key': key,
                    'error': str(e)
                })

        return JsonResponse({
            'status': 'success',
            'current_session_key': request.session.session_key,
            'sessions': sessions,
            'all_redis_keys': all_keys
        })

    except Exception as e:
        print(f"\nError in debug_redis_sessions: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



def test_redis_connection(request):
    """Тестовая функция для проверки работы Redis"""
    try:
        # Тестовая запись
        cache.set('test_key', {'user_id': 1, 'test_data': 'hello'}, timeout=60)

        # Чтение
        data = cache.get('test_key')

        return JsonResponse({
            'status': 'success',
            'data_written': {'user_id': 1, 'test_data': 'hello'},
            'data_read': data,
            'keys_in_redis': cache.keys('*')
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class CheckSessionView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                'is_authenticated': True,
                'username': request.user.username,
                'session_key': request.session.session_key
            })
        return Response({
            'is_authenticated': False,
            'session_key': request.session.session_key if request.session else None
        })


class GetCSRFToken(APIView):
    def get(self, request):
        response = Response()
        origin = request.headers.get('Origin')
        if origin in ["http://localhost:5173", "http://127.0.0.1:5173"]:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
        get_token(request)  # Это установит CSRF cookie
        return response

class MyClass1View(APIView):
    def options(self, request, *args, **kwargs):
        response = Response()
        origin = request.headers.get('Origin')
        if origin in ["http://localhost:5173", "http://127.0.0.1:5173"]:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken'
        return response
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
                    # if user is not None:
                    #     login(request, user)
                    #     print(f"Auth successful for {user.username}")
                    #     print(f"Session after login: {request.session.session_key}")
                    #     print(f"Session data: {dict(request.session)}")
                    #     return Response(f"AuthorizationOK-{user.access_type.access_type_descr}")
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


class LawsListView(APIView):
    def get(self, request):
        print('Get request for a list of laws ')
        # Получение списка объектов (законов)
        laws = Laws.objects.all().order_by('law_date')
        # Создание json для ответа клиенту?
        serializer = LawsSerializer(laws, many=True)
        print(f'Вывод списка законов пользователю: {serializer.data}')
        return Response(serializer.data)

# Список статей закона
class LawArticlesListView(APIView):
    def get(self, request, p_law_id):
        print(f'Get request for a list of articles of {p_law_id} law ')
        # Получение списка статей закона
        articles = Articles.objects.filter(article_parent_id=p_law_id)
        print(f'Articles of law list is: {articles}')

        # Создание json для ответа клиенту?
        serializer = ArticlesShortSerializer(articles, many=True)
        data_list_dict = serializer.data

        print(f'len(data_list_dict) is {len(data_list_dict)}')

        for i in range(0, len(data_list_dict)):
            print(f'------------------------ i is {i}')

        # Сделаю цикл по статьям закона и в нем уже буду добавлять ответственность
        for i in range(0, len(data_list_dict)):
            print(f'I is: {i}')
            respToArticle = RespToArticles.objects.filter(resp_article_id=data_list_dict[i]['article_id'])
            serializerRespToArticles = RespToArticlesSerializer(respToArticle, many=respToArticle.exists())
            print('serializerRespToArticles is')
            print(f'{serializerRespToArticles.data}')
            str_responsobilitys = ''

            for resp_data in serializerRespToArticles.data:
                if resp_data.get('resp_first_type') == 1:
                    str_responsobilitys += ' Уголовная'
                if resp_data.get('resp_second_type') == 1:
                    str_responsobilitys += ' Административная'
                if resp_data.get('resp_third_type') == 1:
                    str_responsobilitys += ' Гражданская'
                if resp_data.get('resp_fourth_type') == 1:
                    str_responsobilitys += ' Иная'


            print(f'str_responsobilitys is {str_responsobilitys}')
            data_list_dict[i]['article_responsobility'] = str_responsobilitys

        print(f'Вывод списка законов пользователю: {data_list_dict}')
        return Response(serializer.data)

# Текст статьи закона
class ArticleTextListView(APIView):
    def get(self, request, p_law_id, p_article_id):

        print('-------------------------------------------------------------------------')
        print(f'Get request for a articles text. {p_law_id} law, {p_article_id} article')

        #law = Laws.objects.get(law_id=p_law_id)

        article = Articles.objects.get(article_number=p_article_id, article_parent_id = p_law_id)
        # Пункты статьи
        articleClauses = ArticleClauses.objects.filter(clause_parent_id=article)
        # Сериалайзер пунктов
        serializer = ArticleClausesSerializer(articleClauses, many=True)
        all_text = ''
        for el in serializer.data:
            print(f'el is {el}')
            all_text = f'{all_text}\n'
            all_text = f'{all_text}Пункт статьи номер: {el['clause_number']}.\n'
            all_text = f'{all_text}Текст пункта статьи: {el['clause_text']}^;.'
        print('Текст, отправляемый обратно:')
        color_print(all_text, 'blue')

        #print(f'serializer.data is: {serializer.data}')
        return Response(all_text)


# Функция добавление новой статьи закону
class NewArticle(APIView):
    def post(self, request, p_law_id):
        data = request.data
        print('Запрос на добавление статьи')
        print(data)
        print(f'p_law_id is: {p_law_id}')
        articleTitle = data['articleTitle']
        print(f'articleTitle is: {articleTitle}')
        points = data['points']
        print(f'points is: {points}')
        responsibilities = data['responsibilities']

        # Нужно получить новый номер статьи. Взять прошлый максимальный и добавить к нему 1
        law = Laws.objects.get(law_id=p_law_id)
        articles = Articles.objects.filter(article_parent_id=law)
        print(f'Articles of law list is: {articles}')
        serializer = ArticlesShortSerializer(articles, many=True)
        print(f'Вывод списка законов пользователю: {serializer.data}')
        print(f'max_number is: {articles.aggregate(Max('article_number'))['article_number__max']}')

        if articles.aggregate(Max('article_number'))['article_number__max'] is None:
            new_article_number = 1
        else:
            new_article_number = articles.aggregate(Max('article_number'))['article_number__max'] + 1


        print(f'responsibilities is: {responsibilities}')
        new_article = Articles.objects.create(
            article_parent_id = law,
            article_number = new_article_number,
            article_title = articleTitle
        )

        i = 1
        # Цикл по пунктам статьи
        for el in points:
            print('Добавление пункта статьи')
            print(f'el is: {el}')
            clause_number = i
            clause_text = el['text']
            ArticleClauses.objects.create(
                clause_number = clause_number,
                clause_parent_id = new_article,
                clause_text = clause_text
            )
            i = i + 1

        resp_first_type  = 0
        resp_second_type = 0
        resp_third_type  = 0
        resp_fourth_type = 0

        if responsibilities['criminal']:
            resp_first_type = 1
        if responsibilities['administrative']:
            resp_second_type = 1
        if responsibilities['civil']:
            resp_third_type = 1
        if responsibilities['other']:
            resp_fourth_type = 1

        RespToArticles.objects.create(
            resp_article_id = new_article
            ,resp_first_type = resp_first_type
            ,resp_second_type = resp_second_type
            ,resp_third_type = resp_third_type
            ,resp_fourth_type = resp_fourth_type
        )

        return Response('NewArticleOK')

