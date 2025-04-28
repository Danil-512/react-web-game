import os
from django.conf import settings
from django.http import FileResponse, HttpResponseBadRequest

from os import error
from rest_framework.views import APIView

# Модели и сериалайзеры для работы с законами и статьями
from .models import MyClass1, Laws, Articles, UsersAccess
from .serializer import MyClass1Serializer, LawsSerializer, ArticlesSerializer, LawsShortSerializer, ArticlesShortSerializer

# Модели и сериалайзеры для работы с авторизацией и регистрацией пользователей
from .models import UsersList, UsersInfo, UsersAuthorization
from .serializer import UsersListSerializer, UsersInfoSerializer, UsersAuthorizationSerializer

# Отвечает за отправляемые по сети данные
from rest_framework.response import Response

# Импорт моих функций
from .functions_to_auth_and_reg import add_new_user, access_type_create



class MyClass1View(APIView):
    def post(self, request):
        #access_type_create(1, 'standart')
        #add_new_user('danilq', 'qwerty')
        print("-----------------------------------------")
        print("Request data:", request.data)  # Логируем данные запроса
        serializer = MyClass1Serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            v_type = serializer.validated_data['type']
            print(f'Получен запрос типа: {v_type}')


            if v_type == "register":
                v_login = serializer.validated_data['data1']
                v_password = serializer.validated_data['data2']

                if len(v_password) < 6 or len(v_login) < 6:
                    print("Слишком короткий пароль или логин. Ошибка. Введите от 8 символов.")
                    return Response('RegisterNOTOK')

                print("Запрос на регистрацию")

                try:
                    user_list_id = UsersList.objects.get(userLogin=v_login)
                    print("Попытка регистрации пользователя с неоригинальным логином")

                except:
                    print("Попытка регистрации пользователя с оригинальным логином")
                    try:
                        add_new_user(v_login, v_password)
                        print(f"Удачная регистрация пользователя: {v_login}")
                        return Response("RegisterOK")
                    except:
                        print("Ошибка регистрации")

            if v_type == "exit":
                print("Запрос на выход из аккаунта")
                return Response("ExitOK")

            if v_type == "authorization":
                v_login = serializer.validated_data['data1']
                v_password = serializer.validated_data['data2']
                print("Запрос на авторизацию")

                try:
                    user_list_id = UsersList.objects.get(userLogin=v_login)
                    print(f"Попытка авторизации существующего пользователя: {v_login}")
                    data1 = UsersAuthorization.objects.get(userId=user_list_id)
                    try:

                        user_password_id = UsersAuthorization.objects.get(userId=user_list_id)
                        user_access_level = UsersAccess.objects.get(userId=user_list_id)
                        print(user_access_level.accessTypeId.accessTypeDescr)
                        print(user_password_id.userPassword)
                        if v_password == user_password_id.userPassword:
                            print("Правильный пароль")
                            print(f'AuthorizationOK-{user_access_level.accessTypeId.accessTypeDescr}')
                            return_string = f'AuthorizationOK-{user_access_level.accessTypeId.accessTypeDescr}'
                            return Response(return_string)
                        else:
                            print("Неправильный пароль")
                            return Response("Authorization-NOTOK")
                    except:
                        print("Ошибка проверки пароля.")


                except(error):
                    print(f"Попытка авторизации несуществующего пользователя: {v_login}")
                    print(error)

            print("-----------------------------------------")
            return Response(serializer.data)
        else:
            print("Serializer errors:", serializer.errors)  # Логируем ошибки сериализатора
            print("-----------------------------------------")
            return Response(serializer.errors, status=400)


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
        print(f'Вывод списка законов пользователю: {serializer.data}')
        return Response(serializer.data)

# Текст статьи закона
class ArticleTextListView(APIView):
    def get(self, request, p_law_id, p_article_id):
        print(f'Get request for a articles text. {p_law_id} law, {p_article_id} article')

        file_path = f'../lawsArticles/1-1.txt'

        # Собираем абсолютный путь
        base_dir = settings.BASE_DIR  # Получаем корневую директорию проекта
        file_path = os.path.abspath(os.path.join(
            base_dir,
            'lawsArticles',  # Целевая директория
            f'{p_law_id}-{p_article_id}.txt'  # Файл
        ))

        # Проверка существования файла (раскомментируйте!)
        if not os.path.exists(file_path):
            return HttpResponseBadRequest(f'File not found: {file_path}')

        # Открываем файл в БИНАРНОМ режиме для чтения
        with open(file_path, 'rb') as file:
            text = file.read()
            print(f'File read is: {text}')
            return Response({'text':text})
        # Проверка существования файла
        #if not os.path.exists(file_path):
         #   return HttpResponseBadRequest('File not found')
        # Открываю файл
        # with open (file_path, 'rb') as file:
        #     print(file.read())
        #     response = FileResponse(file.read())
        #     return response


# class LawStView(APIView):
#     def get(self, request, law_id):
#         try:
#             law = Law.objects.get(pk=law_id)
#             articles = law.articles.all().order_by('id')
#             serializer = LawArticleSerializer(articles, many=True)
#             return Response(serializer.validated_data["id"])
#         except Law.DoesNotExist:
#             return Response({"error": "Law not found"}, status=404)

#
# class LawArticlesView(APIView):
#     def get(self, request, law_id):
#         try:
#             law = Law.objects.get(pk=law_id)
#             articles = law.articles.all().order_by('id')
#             serializer = LawArticleShortSerializer(articles, many=True)
#             print(f"serializer.data is: {serializer.data}")
#             return Response(serializer.data)
#         except Law.DoesNotExist:
#             return Response({"error": "Law not found"}, status=404)
#
# class LawArticleDetailView(APIView):
#     def get(self, request, law_id, str2):
#         try:
#             print(str2)
#             law = Law.objects.get(pk=law_id)
#             articles = law.articles.all().order_by('id')
#             article = articles.filter(id=str2)
#             serializer = LawArticleSerializer(article, many=True)
#             return Response(serializer.data)
#         except Law.DoesNotExist:
#             return Response({"error": "Law not found"}, status=404)
#
# class LawArticlesView2(APIView):
#     def get(self, request, law_id):
#         try:
#             law = Law.objects.get(pk=law_id)
#             articles = law.articles.all().order_by('id')
#             serializer = LawArticleShortSerializer(articles, many=True)
#             return Response(serializer.data)  # Должен возвращать массив
#         except Law.DoesNotExist:
#             return Response({"error": "Law not found"}, status=404)