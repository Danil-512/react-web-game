from django.shortcuts import render
from rest_framework.views import APIView
from .models import MyClass
from .serializer import MyClassSerializer
# Отвечает за отправляемые по сети данные
from rest_framework.response import Response

class MyClassView(APIView):
    # Отправяет список со всеми объектами
    # Создает новый объект на основе данных из тела запроса
    def get(self, request):
        #MyClass.objects.create(title='Python', content='Python')
        output = [
            {
                "title": output.title,
                "content": output.content
            } for output in MyClass.objects.all()
        ]
        return Response(output)

    def post(self, request):
        print("Request data:", request.data)  # Логируем данные запроса
        serializer = MyClassSerializer(data=request.data)
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



