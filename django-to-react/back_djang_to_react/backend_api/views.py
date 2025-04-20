from os import error

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from numpy.ma.core import outer
from rest_framework import status
from rest_framework.views import APIView
from tinycss2 import serialize

from .models import MyClass1, Law, LawArticle
from .serializer import MyClass1Serializer, LawSerializer, LawArticleSerializer, LawArticleShortSerializer

from .models import UsersAuthorization
from .serializer import UsersAuthorizationSerializer

from .models import UsersList
from .serializer import UsersListSerializer

from .models import UsersInfo
from .serializer import UsersInfoSerializer

# Отвечает за отправляемые по сети данные
from rest_framework.response import Response

# Импорт моих функций
from .functions_to_auth_and_reg import add_new_user, access_type_create


class MyClass1View(APIView):
    def get(self, request):
        print("-----------------------------------------")
        print("Request data:", request.GET.get('type'))  # Логируем данные запроса
        #print("Request data:", request.data)  # Логируем данные запроса
        serializer = MyClass1Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            v_type = serializer.validated_data['type']
            print(f'Получен запрос типа: {v_type}')
            if v_type == "authorization":
                v_login = serializer.validated_data['data1']
                v_password = serializer.validated_data['data2']
                print("Запрос на авторизацию")
                all_users_dict = dict()
                all_user = UsersAuthorization.objects.all()
                for obj in all_user:
                    print(obj.userLogin)
                    all_users_dict[f'{obj.userLogin}'] = obj.userPassword
                if v_login in all_users_dict:
                    print(f"Попытка авторизации существующего пользователя: {v_login}")
                    if v_password == all_users_dict[f'{v_login}']:
                        print("Правильный пароль")
                        return Response("AuthorizationOK")
                    else:
                        print("Неправильный пароль")
                        return Response("AuthorizationNOTOK")

                else:
                    print(f"Попытка авторизации несуществующего пользователя: {v_login}")
                # else:
                #    print(f"Ошибка регистрации пользователя с логином: {v_login}")


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
                        print(user_password_id.userPassword)
                        if v_password == user_password_id.userPassword:
                            print("Правильный пароль")
                            return Response("AuthorizationOK")
                        else:
                            print("Неправильный пароль")
                            return Response("AuthorizationNOTOK")
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

class LawListView(APIView):
    def get(self, request):
        laws = Law.objects.all().order_by('date')
        serializer = LawSerializer(laws, many=True)
        return Response(serializer.data)

# class LawArticlesView(APIView):
#     def get(self, request, law_id):
#         try:
#             law = Law.objects.get(pk=law_id)
#             articles = law.articles.all().order_by('id')
#             serializer = LawArticleSerializer(articles, many=True)
#             return Response(serializer.data)
#         except Law.DoesNotExist:
#             return Response(
#                 {"error": "Law not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#
# class LawArticlesView(APIView):
#     def get(self, request, law_id):
#         try:
#             law = Law.objects.get(pk=law_id)
#             articles = law.articles.all().order_by('id')
#
#             # # Добавим пагинацию
#             # page = self.paginate_queryset(articles)
#             # if page is not None:
#             #     serializer = LawArticleSerializer(page, many=True)
#             #     return self.get_paginated_response(serializer.data)
#
#             serializer = LawArticleSerializer(articles, many=True)
#             return Response(serializer.data)
#
#         except ObjectDoesNotExist:
#             return Response(
#                 {"error": "Law not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except Exception as e:
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

class LawStView(APIView):
    def get(self, request, law_id):
        try:
            law = Law.objects.get(pk=law_id)
            articles = law.articles.all().order_by('id')
            serializer = LawArticleSerializer(articles, many=True)
            return Response(serializer.validated_data["id"])
        except Law.DoesNotExist:
            return Response({"error": "Law not found"}, status=404)


class LawArticlesView(APIView):
    def get(self, request, law_id):
        try:
            law = Law.objects.get(pk=law_id)
            articles = law.articles.all().order_by('id')
            serializer = LawArticleShortSerializer(articles, many=True)
            print(f"serializer.data is: {serializer.data}")
            return Response(serializer.data)
        except Law.DoesNotExist:
            return Response({"error": "Law not found"}, status=404)

    # def get(self, request, law_id):
    #     try:
    #         law = Law.objects.get(pk=law_id)
    #         articles = law.articles.all().order_by('id')
    #         serializer = LawArticleSerializer(articles, many=True)
    #         return Response(serializer.data)
    #     except Law.DoesNotExist:
    #         return Response({"error": "Law not found"}, status=404)

class LawArticleDetailView(APIView):
    def get(self, request, law_id, str2):
        try:
            print(str2)
            law = Law.objects.get(pk=law_id)
            articles = law.articles.all().order_by('id')
            article = articles.filter(id=str2)
            serializer = LawArticleSerializer(article, many=True)
            return Response(serializer.data)
        except Law.DoesNotExist:
            return Response({"error": "Law not found"}, status=404)
        # try:
        #
        #     article = LawArticle.objects.get(pk=article_id)
        #     serializer = LawArticleSerializer(article)  # используем полный сериализатор
        #     return Response(serializer.data)
        # except LawArticle.DoesNotExist:
        #     return Response({"error": "Article not found"}, status=404)

class LawArticlesView2(APIView):
    def get(self, request, law_id):
        try:
            law = Law.objects.get(pk=law_id)
            articles = law.articles.all().order_by('id')
            serializer = LawArticleShortSerializer(articles, many=True)
            return Response(serializer.data)  # Должен возвращать массив
        except Law.DoesNotExist:
            return Response({"error": "Law not found"}, status=404)