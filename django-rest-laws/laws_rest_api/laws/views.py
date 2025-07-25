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
    renderer_classes = [JSONRenderer]  # Явное указание шаблона рендера. Без этого, restfr не знает какой выбрать

    # Документация swagger
    @swagger_auto_schema(
        operation_description = "Добавление новой статьи к закону",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
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
            400: 'Неверные параметры запроса'
        }
    )


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
