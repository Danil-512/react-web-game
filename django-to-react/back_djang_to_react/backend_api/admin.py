from django.contrib import admin

from django.contrib import admin
#from .models import (Laws, Articles)
#, LawsArticles)

from backend_api.models import *

# Register your models here.
# admin.site.register(UsersList)
# admin.site.register(UsersAuthorization)
# admin.site.register(UsersInfo)
#
# class LawArticleInline(admin.TabularInline):
#     model = LawsArticles
#     extra = 1  # Количество пустых форм для добавления статей
#
# @admin.register(Law)
# class LawAdmin(admin.ModelAdmin):
#     list_display = ('number', 'title', 'date')  # Отображаемые поля в списке
#     search_fields = ('title', 'number')  # Поля для поиска
#     list_filter = ('date',)  # Фильтры справа
#     inlines = [LawArticleInline]  # Встроенное редактирование статей
#
# @admin.register(LawArticle)
# class LawArticleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'law', 'date')  # Отображаемые поля
#     list_filter = ('law', 'date')  # Фильтры
#     search_fields = ('title', 'text')  # Поиск
#     date_hierarchy = 'date'  # Иерархия по дате
#

