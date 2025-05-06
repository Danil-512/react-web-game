import os
from django.conf import settings
from django.http import FileResponse, HttpResponseBadRequest

from os import error
from rest_framework.views import APIView
from django.db.models import Max

# Модели и сериалайзеры для работы с законами и статьями
from .models import MyClass1, Laws, Articles, UsersAccess, ArticleClauses, RespToArticles
from .serializer import MyClass1Serializer, LawsSerializer, ArticlesSerializer, LawsShortSerializer, ArticlesShortSerializer, ArticleClausesSerializer

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

        article = Articles.objects.get(article_id=p_article_id)
        # Пункты статьи
        articleClauses = ArticleClauses.objects.filter(clause_parent_id=article)
        # Сериалайзер пунктов
        serializer = ArticleClausesSerializer(articleClauses, many=True)
        all_text = ''
        for el in serializer.data:
            print(f'el is {el}')
        print(f'serializer.data is: {serializer.data}')


        return Response('NewArticleOK')

        # file_path = f'../lawsArticles/1-1.txt'
        #
        # # Собираем абсолютный путь
        # base_dir = settings.BASE_DIR  # Получаем корневую директорию проекта
        # file_path = os.path.abspath(os.path.join(
        #     base_dir,
        #     'lawsArticles',  # Целевая директория
        #     f'{p_law_id}-{p_article_id}.txt'  # Файл
        # ))
        #
        # # Проверка существования файла (раскомментируйте!)
        # if not os.path.exists(file_path):
        #     return HttpResponseBadRequest(f'File not found: {file_path}')
        #
        # # Открываем файл в БИНАРНОМ режиме для чтения
        # with open(file_path, 'rb') as file:
        #     text = file.read()
        #     print(f'File read is: {text}')
        #     return Response({'text':text})
        # # Проверка существования файла
        # #if not os.path.exists(file_path):
        #  #   return HttpResponseBadRequest('File not found')
        # # Открываю файл
        # # with open (file_path, 'rb') as file:
        # #     print(file.read())
        # #     response = FileResponse(file.read())
        # #     return response

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
