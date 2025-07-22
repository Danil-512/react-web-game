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
    article_number         = models.IntegerField (blank=False)
    article_title          = models.CharField    (blank=False, max_length=100)
    article_descr          = models.CharField    (blank=False, max_length=400, default='')
    #
    # Название таблицы в базе данных - список статей законов
    class Meta:
        db_table = 'rest_articles'

# Модель с пунктами статей
class ArticleClauses(models.Model):
    clause_id              = models.AutoField    (primary_key=True)
    clause_number          = models.IntegerField (blank=False, default=0)
    clause_parent_id       = models.ForeignKey   (Articles, to_field='article_id', on_delete=models.CASCADE, blank=False, default=0)
    clause_text            = models.CharField    (blank=False, max_length=2000)
    #
    # Название таблицы в базе данных - список пунктов статей
    class Meta:
        db_table = 'rest_articles_clauses'

# Модель с видами ответственности
class Responsibilitys(models.Model):
    responsibility_id      = models.IntegerField (primary_key=True)
    responsibility_type    = models.CharField    (blank=False, max_length=50)
    #
    # Название таблицы в базе данных - виды ответственности за нарушение статей
    class Meta:
        db_table = 'rest_responsibilitys'

# # Модель с ответственностью за нарушение законов
# class RespToLaws(models.Model):
#     resp_law_record_id = models.IntegerField(primary_key=True)
#     resp_law_id        = models.ForeignKey(Laws, to_field='law_id', blank=False, on_delete=models.CASCADE)
#     resp_first_type    = models.IntegerField(blank=False, default=0)
#     resp_second_type   = models.IntegerField(blank=False, default=0)
#     resp_third_type    = models.IntegerField(blank=False, default=0)
#     resp_fourth_type   = models.IntegerField(blank=False, default=0)
#     resp_another_type  = models.IntegerField(blank=False, default=0)
#     resp_none_type     = models.IntegerField(blank=False, default=0)
#     class Meta:
#         db_table = 'rest_resp_to_laws'

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