from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import *
from rest_framework.renderers import JSONRenderer

from .models import Laws, Articles, ArticleClauses, RespToArticles
from .serializer import LawsSerializer, ArticlesShortSerializer, ArticleClausesSerializer, RespToArticlesSerializer

# Эти импорты будут использоваться для ведения документации по методам (url-адресам, к которым привязаны эти методы)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Функция для цветного вывода в консоль
def color_print(text, color):
    if   color.upper() == 'BLUE':
        print("\033[34m{}".format(text))
    elif color.upper() == 'RED':
        print("\033[31m{}".format(text))
    else:
        print("\033[33m{}".format(text))
    print("\033[0m{}".format(''))

# Получение списка законов - первая страница
class LawsListView(APIView):
    renderer_classes = [JSONRenderer] # Явное указание шаблона рендера. Без этого, restfr не знает какой выбрать
    def get(self, request):
        print('Get request for a list of laws ')
        # Получение списка законов
        laws = Laws.objects.all().order_by('law_date')
        # Создание json для ответа клиенту?
        serializer = LawsSerializer(laws, many=True)
        print(f'Вывод списка законов пользователю: {serializer.data}')
        return Response(serializer.data)

# Получение списка статей закона
class LawArticlesListView(APIView):
    renderer_classes = [JSONRenderer] # Явное указание шаблона рендера. Без этого, restfr не знает какой выбрать
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
        print('\n-------------------------------------------------------------------------')
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
                        "message": "NewArticleOK"
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
        print('\n-------------------------------------------------------------------------')
        print(f'Post request for adding a new article to the law. {p_law_id} law')
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
        # Создание новой статьи в базе + получение переменной с ее данными
        new_article = Articles.objects.create(
            article_parent_id = p_law_id,
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
        #
        RespToArticles.objects.create(
            resp_article_id  = new_article
           ,resp_first_type  = 1 if responsibilities['criminal'] else 0
           ,resp_second_type = 1 if responsibilities['administrative'] else 0
           ,resp_third_type  = 1 if responsibilities['civil'] else 0
           ,resp_fourth_type = 1 if responsibilities['other'] else 0
        )

        return Response('NewArticleOK')
