from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# класс для отображения в админ-панели
class WomenAdmin(admin.ModelAdmin):
    # полный список опций
    # https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#modeladmin-options
    # перечень атрибутов для отображения в списке записей
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    # кликабельные поля
    list_display_links = ('id', 'title')
    # по каким полям можно производить поиск.
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    # автоматическое формирование слага
    prepopulated_fields = {"slug": ("title",)}
    # атрибут fields - порядок и список редактируемых полей в форме редактирования
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    # добавление не редактируемых полей в форме редактирования
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    # перемещение кнопок сохранения наверх
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            # mark_safe - возврат строки без экранирования
            return mark_safe(f"<img src='{object.photo.url}' width=50>")
        # если фото не будет найдено, Джанго автоматически подставит прочерк "-"

    # задание кастомного заголовка для созданной функции
    get_html_photo.short_description = "Миниатюра"

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


# Дополнительные атрибуты для тонкой настройки админ-панели
# https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#adminsite-attributes
admin.site.site_title = "Админ-панель сайта Women"
admin.site.site_header = "Админ-панель сайта Women"

