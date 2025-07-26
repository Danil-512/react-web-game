from django.db import models

# Модель с законами
class Laws(models.Model):
    law_id                 = models.AutoField    (primary_key=True)
    law_number             = models.CharField    (blank=False, max_length=20, verbose_name="Номер закона", unique=True)
    law_title              = models.CharField    (blank=False, max_length=400, verbose_name="Название закона")
    law_date               = models.DateField    (verbose_name="Дата принятия")
    #
    # Строковое представление модели для отображения в админ панели и логах
    def __str__(self):
        return f"{self.law_number} - {self.law_title}"
    #
    # Название таблицы в базе данных - список законов
    class Meta:
        db_table = 'rest_laws'

# Модель со статьями закона
class Articles(models.Model):
    article_id             = models.AutoField    (primary_key=True)
    article_parent_id      = models.ForeignKey   (Laws, to_field='law_id', on_delete=models.CASCADE, blank=False, default=0)
    article_number         = models.IntegerField (blank=True)
    article_title          = models.CharField    (blank=False, max_length=100)
    article_descr          = models.CharField    (blank=False, max_length=400, default='')
    #
    # Механизм присвоения нового номера статьи относительно закона (если номер статьи не был передан)
    def save(self, *args, **kwargs):
        if not self.article_number:
            # Получение списка статей закона
            articles_list = Articles.objects.filter(article_parent_id=self.article_parent_id)
            #
            # Получение максимального номера статьи
            max_number = articles_list.aggregate(models.Max('article_number'))['article_number__max']
            #
            # Присвоение статье номера
            self.article_number = (max_number or 0) + 1
            #
        # Сохранение
        super().save(*args, **kwargs)
    #
    # Название таблицы в базе данных - список статей законов
    class Meta:
        db_table = 'rest_articles'
        unique_together = [['article_parent_id', 'article_number']] # Ограничение, что статьи уникальны относительно их номера и закона вместе

# Модель с пунктами статей
class ArticleClauses(models.Model):
    clause_id              = models.AutoField    (primary_key=True)
    clause_number          = models.IntegerField (blank=True)
    clause_parent_id       = models.ForeignKey   (Articles, to_field='article_id', on_delete=models.CASCADE, blank=False)
    clause_text            = models.CharField    (blank=False, max_length=2000)
    #
    # Механизм присвоения нового номера пункта статьи относительно закона (если номер пункта статьи не был передан)
    def save(self, *args, **kwargs):
        if not self.clause_number:
            # Получение списка пунктов статьи
            clauses_list = ArticleClauses.objects.filter(clause_parent_id=self.clause_parent_id)
            #
            # Получение максимального номера пункта
            max_number = clauses_list.aggregate(models.Max('clause_number'))['clause_number__max']
            #
            # Присвоение статье номера
            self.clause_number = (max_number or 0) + 1
            #
        # Сохранение
        super().save(*args, **kwargs)
    #
    # Название таблицы в базе данных - список пунктов статей
    class Meta:
        db_table = 'rest_articles_clauses'
        unique_together = [['clause_parent_id','clause_number']]  # Ограничение, что пункты уникальны относительно их номера и статьи вместе

# Модель с видами ответственности
class ResponsibilityTypes(models.Model):
    responsibility_id      = models.IntegerField (primary_key=True)
    responsibility_type    = models.CharField    (blank=False, max_length=50)
    responsibility_descr   = models.CharField    (blank=True, max_length=150)
    #
    # Проверка наличия данных и заполнение данными
    # (Забивать в коде данные для базы данных идея не лучшая, но для удобства сделаю так. Тем более, что эти типы ответственности не изменятся)
    def save(self, *args, **kwargs):
        # Сохранение
        super().save(*args, **kwargs)
        #
        # Проверка на то, нужно ли добавлять стандартные записи
        if not ResponsibilityTypes.objects.exists():
            # Стандартные типы ответственности:
            default_types = [
                (1, 'CRIMINAL', 'Уголовная ответственность')
               ,(2, 'ADMINISTRATIVE', 'Административная ответственность')
               ,(3, 'CIVIL', 'Гражданская ответственность')
               ,(4, 'FINANCIAL', 'Материальная ответственность')
               ,(5, 'OTHER', 'Иная ответственность')
            ]
            #
            # Заполнение таблицы
            for resp_id, resp_type, resp_descr in default_types:
                ResponsibilityTypes.objects.get_or_create(
                    responsibility_id    = resp_id
                   ,responsibility_type  = resp_type
                   ,responsibility_descr = resp_descr
                )
    #
    # Название таблицы в базе данных - виды ответственности за нарушение статей
    class Meta:
        db_table = 'rest_responsibility_types'


# Модель с ответственностью за нарушение статей законов
class RespToArticles(models.Model):
    resp_article_record_id = models.AutoField    (primary_key=True)
    resp_article_id        = models.ForeignKey   (Articles, to_field='article_id', blank=False, on_delete=models.CASCADE)
    resp_first_type        = models.IntegerField (blank=False, default=0)
    resp_second_type       = models.IntegerField (blank=False, default=0)
    resp_third_type        = models.IntegerField (blank=False, default=0)
    resp_fourth_type       = models.IntegerField (blank=False, default=0)
    resp_another_type      = models.IntegerField (blank=False, default=0)
    #
    # Название таблицы в базе данных - ответственности за нарушение статей
    class Meta:
        db_table = 'rest_resp_to_articles'