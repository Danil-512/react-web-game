from django.shortcuts import render
from numpy.ma.core import outer
from rest_framework.views import APIView
from tinycss2 import serialize

from .models import MyClass1
from .serializer import MyClass1Serializer

from .models import UsersAuthorization
from .serializer import UsersAuthorizationSerializer

from .models import UsersList
from .serializer import UsersListSerializer

from .models import UsersInfo
from .serializer import UsersInfoSerializer

# Отвечает за отправляемые по сети данные
from rest_framework.response import Response


class MyClass1View(APIView):
    # Отправяет список со всеми объектами
    # Создает новый объект на основе данных из тела запроса
    def get(self, request):
        #MyClass1.objects.create(type='Python', data1='Python', data2='2', data3='2')
        #MyClass1.objects.all().delete()

        # Получение данных из моделей
        all_user = UsersList.objects.all()
        print(all_user)



        if MyClass1.objects.all():
            all_myClass = MyClass1.objects.all()
            output = []
            for output1 in all_myClass:
                output.append(
                    {
                        "type": output1.type
                        , "data1": output1.data1
                        , "data2": output1.data2
                        , "data3": output1.data3
                    }
                )
            return Response(output)
        return ""


    def post(self, request):
        print("-----------------------------------------")
        print("Request data:", request.data)  # Логируем данные запроса
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
                #else:
                #    print(f"Ошибка регистрации пользователя с логином: {v_login}")





            #serializer.save()
            print("-----------------------------------------")
            return Response(serializer.data)
        else:
            print("Serializer errors:", serializer.errors)  # Логируем ошибки сериализатора
            print("-----------------------------------------")
            return Response(serializer.errors, status=400)

