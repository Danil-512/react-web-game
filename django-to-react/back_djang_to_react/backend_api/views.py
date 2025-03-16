from django.shortcuts import render
from rest_framework.views import APIView
from .models import MyClass1
from .serializer import MyClass1Serializer
# Отвечает за отправляемые по сети данные
from rest_framework.response import Response

class MyClass1View(APIView):
    # Отправяет список со всеми объектами
    # Создает новый объект на основе данных из тела запроса
    def get(self, request):
        MyClass1.objects.create(type='Python', data1='Python', data2='2', data3='2')
        #MyClass1.objects.all().delete()
        for output in MyClass1.objects.all():
            if output.data2 == "":
                output = [
                    {
                        "type": output.type,
                        "data1": output.data1,
                        "data2": "null",
                        "data3": "null",
                    }
                ]
            elif output.data3 == "":
                output = [
                    {
                        "type": output.type,
                        "data1": output.data1,
                        "data2": output.data2,
                        "data3": "null",
                    }
                ]
            elif output.type != "" and output.data1 != "":
                output = [
                    {
                        "type": output.type,
                        "data1": output.data1,
                        "data2": output.data2,
                        "data3": output.data3,
                    }
                ]
            return Response(output)

    def post(self, request):
        print("Request data:", request.data)  # Логируем данные запроса
        serializer = MyClass1Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            print("Serializer errors:", serializer.errors)  # Логируем ошибки сериализатора
            return Response(serializer.errors, status=400)
        # serializer = MyClassSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     return Response(serializer.data)



