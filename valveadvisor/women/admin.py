from django.contrib import admin

from .models import *


# класс для отображения в админ-панели
class WomenAdmin(admin.ModelAdmin):
    # перечень атрибутов для отображения в списке записей
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    # кликабельные поля
    list_display_links = ('id', 'title')
    # по каким полям можно производить поиск.
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    prepopulated_fields = {"slug": ("name", )}


# Функция get_absolute_url в модели автоматически добавляет кнопку "Смотреть на сайте" в админ-панель.
# Она используется многими компонентами Django, поэтому ее лучше всегда прописывать.
# Если выше прописан специальный класс для работы с админ-панелью, его надо указывать явно при регистрации.
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)


