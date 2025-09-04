from datetime import datetime

import datetime as dt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import Laws, Articles, ArticleClauses, RespToArticles
from .serializer import LawsSerializer, ArticlesShortSerializer, ArticleClausesSerializer, RespToArticlesSerializer

# Эти импорты будут использоваться для ведения документации по методам (url-адресам, к которым привязаны эти методы)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Импорт для использования стандартных htpp статусов в ответах
from rest_framework import status


# Функция для цветного вывода в консоль
def color_print(text, color):
    if   color.upper() == 'BLUE':
        print("\033[34m{}".format(text))
    elif color.upper() == 'RED':
        print("\033[31m{}".format(text))
    else:
        print("\033[33m{}".format(text))
    print("\033[0m{}".format(''))

# Функция для получения статуса подключения к базам
class HealthCheck(APIView):
    def get(self, request):
        response_data = {
            "status": "healthy",
            "database": "connected",
            "redis": "connected",
            "timestamp": "time.time()"
        }
        #
        return Response(response_data)

# Функция для создания первого закона - без него приложение не работает (В будущем надо будет это исправить и реализовать возможность добавлять законы).
def check_first_law_existence():
    #
    # Проверка наличия законов
    existence_fact = Laws.objects.exists()
    #
    if existence_fact:
        return
    else:
        # Законов в базе нет - нужно создать первый
        first_law = Laws.objects.create(
            law_number = '149-ФЗ',
            law_title  = 'Об информации, информационных технологиях и о защите информаци',
            law_date   = dt.date(2006, 7, 27)
        )



# Получение списка законов - первая страница
class LawsListView(APIView):
    renderer_classes = [JSONRenderer] # Явное указание шаблона рендера. Без этого, restfr не знает какой выбрать
    #
    # Документация swagger
    @swagger_auto_schema(
        operation_description='Получение списка законов',
        responses={
            200: openapi.Response(
                description='Успешный ответ',
                    schema=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='''[{'law_id': 1, 'law_number': '149-ФЗ', 'law_title': 'Об информации, информационных технологиях и о защите информации', 'law_date': '2006-07-27'}]'''
                    )
            ),
            400: 'Ошибка в запросе',
            404: 'Законы не найдены',
            500: 'Ошибка сервера'
        }
    )
    #
    def get(self, request):
        check_first_law_existence()
        #
        color_print('\n/----------------------------------------------------------------------------------\n', 'red')
        print('Get request for a list of laws ')
        #
        # Получение списка законов из базы с сортировкой по дате принятия
        laws = Laws.objects.all().order_by('law_date')
        #
        # Создание json для ответа клиенту
        serializer = LawsSerializer(laws, many=True)
        #
        # Вывод в консоль (в будущем добавить в логирование!)
        print(f'\nВызов метода get класса {self.__class__.__name__}. Отправляемый текст:')
        color_print(serializer.data, 'blue')
        #
        color_print('\n----------------------------------------------------------------------------------/\n', 'red')
        return Response(serializer.data)

# Получение списка статей закона
class LawArticlesListView(APIView):
    renderer_classes = [JSONRenderer] # Явное указание шаблона рендера. Без этого, restfr не знает какой выбрать
    #
    # Документация swagger
    @swagger_auto_schema(
        operation_description='Получение списка статей закона',
        manual_parameters=[
            openapi.Parameter(
                name='p_law_id'
                , in_=openapi.IN_PATH  # Указывает, что параметр встроен в тело url запроса
                , description='Ид закона'
                , type=openapi.TYPE_INTEGER
                , required=True  # Параметр обязателен
                , example=1  # Пример параметра
            )
        ],
        responses={
            200: openapi.Response(
                description='Успешный ответ',
                schema=openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='''[{'article_id': 1, 'article_number': 1, 'article_title': 'Первый пункт статьи', 'article_descr': 'Описание пункта статьи', 'article_responsobility': ' Административная Гражданская'}
                               ,{'article_id': 2, 'article_number': 2, 'article_title': 'Второй пункт статьи', 'article_descr': 'Описание пункта статьи', 'article_responsobility': ' Административная'}]'''
                )
            ),
            400: 'Неверные параметры запроса',
            404: 'Статьи не найдены',
            500: 'Ошибка сервера'
        }
    )
    #
    def get(self, request, p_law_id):
        check_first_law_existence()
        #
        color_print('\n/----------------------------------------------------------------------------------', 'red')
        print(f'Get request for a list of articles of {p_law_id} law ')
        #
        # Получение списка статей закона из базы
        articles = Articles.objects.filter(article_parent_id=p_law_id)
        #
        # Создание json для ответа клиенту
        serializer = ArticlesShortSerializer(articles, many=True)
        data_list_dict = serializer.data
        #
        # Цикл по статьям закона. В нем добавляются ответственности к списку статей
        for article_data in data_list_dict:
            # Получение списка ответвенностей по статьям
            respToArticle = RespToArticles.objects.filter(resp_article_id=article_data['article_id'])
            #
            # Получения списка словарей (json) из данных с базы
            serializerRespToArticles = RespToArticlesSerializer(respToArticle, many=True)
            #
            # Переменная, в которую будут записаны виды ответственности за нарушение статьи
            str_responsobilitys = ''
            #
            # Добавление видов ответственности в переменную
            for resp_data in serializerRespToArticles.data:
                if resp_data.get('resp_first_type') == 1:
                    str_responsobilitys += ' Уголовная'
                if resp_data.get('resp_second_type') == 1:
                    str_responsobilitys += ' Административная'
                if resp_data.get('resp_third_type') == 1:
                    str_responsobilitys += ' Гражданская'
                if resp_data.get('resp_fourth_type') == 1:
                    str_responsobilitys += ' Иная'
            #
            # Добавление в список словаря с ответственностью
            article_data['article_responsobility'] = str_responsobilitys
        #
        # Вывод в консоль (в будущем добавить в логирование!)
        print(f'\nВызов метода get класса {self.__class__.__name__}. Отправляемый текст:')
        color_print(serializer.data, 'blue')
        #
        color_print('----------------------------------------------------------------------------------/\n', 'red')
        return Response(serializer.data)

# Получение текста статьи закона
class ArticleTextListView(APIView):
    renderer_classes = [JSONRenderer]  # Явное указание шаблона рендера. Без этого, restfr не знает какой выбрать
    #
    # Документация swagger
    @swagger_auto_schema(
        operation_description = 'Получение текста статьи закона',
        manual_parameters = [
            openapi.Parameter(
                name        = 'p_law_id'
               ,in_         = openapi.IN_PATH       # Указывает, что параметр встроен в тело url запроса
               ,description = 'Ид закона'
               ,type        = openapi.TYPE_INTEGER
               ,required    = True                  # Параметр обязателен
               ,example     = 1                     # Пример параметра
            ),
            openapi.Parameter(
                name        = 'p_article_id'
               ,in_         = openapi.IN_PATH
               ,description = 'Ид статьи закона'
               ,type        = openapi.TYPE_INTEGER
               ,required    = True
               ,example     = 1
            )
        ],
        responses = {
            200: openapi.Response(
                description = 'Успешный ответ',
                schema = openapi.Schema(
                    type = openapi.TYPE_STRING,
                    example = '''Пункт статьи номер: 1.
                                 Текст пункта статьи: sgrhtdyfghkj^;.
                                 Пункт статьи номер: 2.
                                 Текст пункта статьи: yrtukyilyilukt.'''
                )
            ),
            400: 'Неверные параметры запроса',
            404: 'Статья не найдена',
            500: 'Ошибка сервера'
        }
    )
    #
    def get(self, request, p_law_id, p_article_id):
        check_first_law_existence()
        #
        color_print('\n/----------------------------------------------------------------------------------', 'red')
        print(f'Get request for a articles text. {p_law_id} law, {p_article_id} article')
        #
        # Получение статьи
        article = Articles.objects.get(article_number=p_article_id, article_parent_id = p_law_id)
        #
        # Получение пунктов статьи
        articleClauses = ArticleClauses.objects.filter(clause_parent_id=article)
        #
        # Сериализация полученных пунктов (преобразование в JSON-подобный формат - список словарей)
        serializer = ArticleClausesSerializer(articleClauses, many=True)
        #
        # Переменная для хранения отправляемого теста
        all_text = ''
        #
        # Цикл с заполнением отправляемой переменной
        for el in serializer.data:
            all_text = f'{all_text}Пункт статьи номер: {el['clause_number']}.\n'
            all_text = f'{all_text}Текст пункта статьи: {el['clause_text']}^;.'
        #
        # Вывод в консоль (в будущем добавить в логирование!)
        print(f'\nВызов метода get класса {self.__class__.__name__}. Отправляемый текст:')
        color_print(all_text, 'blue')
        #
        color_print('----------------------------------------------------------------------------------/\n', 'red')
        return Response(all_text)

# Добавление новой статьи закону
class NewArticle(APIView):
    renderer_classes = [JSONRenderer]  # Явное указание шаблона рендера. Без этого, restfr не знает какой выбрать
    #
    # Документация swagger
    @swagger_auto_schema(
        operation_description = "Добавление новой статьи к закону",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            manual_parameters=[
                openapi.Parameter(
                    name='p_law_id'
                    , in_=openapi.IN_PATH
                    , description='Ид закона'
                    , type=openapi.TYPE_INTEGER
                    , required=True
                    , example=1
                ),
            ],
            required=['articleTitle', 'points', 'responsibilities'],
            example={
                "articleTitle": "Новая статья о нарушениях",
                "points": [
                    {"text": "Текст первого пункта статьи"},
                    {"text": "Текст второго пункта статьи"}
                ],
                "responsibilities": {
                    "criminal": True,
                    "administrative": False,
                    "civil": True,
                    "other": False
                }
            }
        ),
        responses={
            200: openapi.Response(
                description='Статья успешно добавлена',
                examples={
                    'application/json': {
                        "message": "Статья успешно добавлена"
                    }
                }
            ),
            400: 'Неверные параметры запроса',
            404: 'Закон не найден',
            500: 'Ошибка сервера'
        }
    )
    #
    def post(self, request, p_law_id):
        check_first_law_existence()
        #
        color_print('\n/----------------------------------------------------------------------------------', 'red')
        print(f'Post request for adding a new article to the law. {p_law_id} law')
        #
        # Проверка вызова ошибки
        # # Ответ в виде стандартного JSON
        # response_data = {
        #     'data': 'Закон не найден',
        #     'status': status.HTTP_404_NOT_FOUND
        # }
        # print(f'response_data is: {response_data}')
        # # Возврат ответа
        # return Response(response_data)
        #
        # Переменная с отправленными фронтом данными
        data = request.data
        #
        # Вывод в консоль (в будущем добавить в логирование!)
        print(f'\nВызов метода post класса {self.__class__.__name__}. Отправляемый текст:')
        color_print(data, 'blue')
        #
        # Создание отдельных переменных на разную информацию из запроса и заполнение данными
        article_title    = data['article_title']
        points           = data['points']
        responsibilities = data['responsibilities']
        #
        # Получение закона из базы - используется как внешний ключ
        try:
            law = Laws.objects.get(law_id = p_law_id)
        except:
            # Ответ в виде стандартного JSON
            response_data = {
                'data':'Закон не найден',
                'status':status.HTTP_404_NOT_FOUND
            }
            print(f'response_data is: {response_data}')
            # Возврат ответа
            return Response(response_data)
        #
        # Создание новой статьи в базе + получение переменной с ее данными
        new_article = Articles.objects.create(
            article_parent_id = law,
            article_title = article_title
        )
        #
        # Цикл по полученным из запроса пунктам статьи - создание новых пунктов в базе
        for el in points:
            clause_text = el['text']
            ArticleClauses.objects.create(
                clause_parent_id = new_article,
                clause_text = clause_text
            )
        #
        # Добавление новой статьи в базу
        RespToArticles.objects.create(
            resp_article_id  = new_article
           ,resp_first_type  = 1 if responsibilities['criminal'] else 0
           ,resp_second_type = 1 if responsibilities['administrative'] else 0
           ,resp_third_type  = 1 if responsibilities['civil'] else 0
           ,resp_fourth_type = 1 if responsibilities['other'] else 0
        )
        #
        color_print('----------------------------------------------------------------------------------/\n', 'red')
        #
        # Ответ в виде стандартного JSON
        response_data = {
            'data': 'Статья успешно добавлена',
            'status': status.HTTP_200_OK
        }
        print(f'response_data is: {response_data}')
        # Возврат ответа
        return Response(response_data)