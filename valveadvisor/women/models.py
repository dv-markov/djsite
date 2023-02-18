# Create your models here
# здесь сохраняются все классы моделей приложения
# пакет models содержит базовые классы моделей, на основании которых можно создавать свои модели таблиц баз данных
from django.db import models
from django.urls import reverse


class Women(models.Model):
    # Поле id уже прописано в классе Model,
    # описание доступных типов полей класса см. в документации: djbook.ru
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    # если класс категорий прописан ниже текущего класса, его имя надо указывать в кавычках.
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return f"{self.title}, id:{self.pk}"

    # более предпочтительный подход для ссылок, связанных с базой данных
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # Дочерний класс для отображения класса в админ-панели
    class Meta:
        verbose_name = "Известные женщины"
        verbose_name_plural = "Известные женщины"
        # обратная сортировка - добавить минус
        # эта сортировка работает не только в админ-панели, но и везде, где перечисляются объекты этого класса
        ordering = ['-time_create', 'title']


# Встроенные классы Django для связи моделей:
# ForeignKey - для связей Many to One (поля отношений)
# ManyToManyField - для связей Many to Many (многие ко многим)
# OneToOneField - для связей One to One (один к одному)

# https://docs.djangoproject.com/en/4.1/topics/db/models/#relationships
# ForeignKey(<ссылка на первичную модель>, on_delete=<ограничения при удалении>)
# Первичная модель - модель категорий
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        # обратная сортировка - добавить минус
        # эта сортировка работает не только в админ-панели, но и везде, где перечисляются объекты этого класса
        ordering = ['id']


# Создание таблицы в базе данных на основе модели.
# Для этого в Джанго существует механизм создания и выполнения миграций для баз данных.

# Миграции - модули языка Python, в которых прописаны команды на уровне ORM-интерфейса
# для создания таблиц определенных структур.

# При выполнении файла миграции в базе данных создаются новые или изменяются существующие таблицы,
# а также связи между ними.
# Каждый новый файл помещается в папке migrations соответствующего приложения.
# На основе файлов миграции создается структура таблиц в базе данных.

# Каждый файл миграции описывает лишь изменения в структуре таблиц, которые произошли с прошлого раза.
# Их можно рассматривать, как контроллеры версии.
# Благодаря этому, можно всегда откатиться к предыдущей структуре
# и продолжить работу с предыдущими связями между таблицами.

# При разработке сайте структуру таблиц лучше продумывать заранее и потом не менять.


# CRUD - Create, Read, Update, Delete
# Система работы с ORM-моделями Django
# ORM - независимость от типа БД и оптимизация скорости выполнения


# Каждый класс модели содержит специальный статический объект - objects
# Он наследуется от базового класса модели Model и представляет собой ссылку на специальный класс-менеджер
# Например, Women.objects






