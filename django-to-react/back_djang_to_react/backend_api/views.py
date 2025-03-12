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
        output = [
            {
                "title": output.title,
                "content": output.content
            } for output in MyClass.objects.all()
        ]
        return Response(output)

    def post(self, request):
        serializer = MyClassSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


