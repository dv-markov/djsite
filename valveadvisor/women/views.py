from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
# render - встроенный шаблонизатор Django

from .models import *

# menu = ["О сайте 🐱‍👤", "Добавить статью 🐱‍🏍", "Обратная связь 🐱‍💻", "Войти 🐱‍🚀"]

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}]


def index(request):  # HttpRequest
    posts = Women.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': "Главная страница"
    }
    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


# def categories(request, catid):
#     if request.GET:
#         print(request.GET)
#     # if request.POST:
#     #     print(request.POST)
#
#     return HttpResponse(f"<h1>Статья по категориям</h1><p>{catid}</p>")
#
#
# def archive(request, year):
#     if int(year) > 2022:
#         #  raise Http404()
#         # return redirect('/')  # временный редирект для перенаправления с кодом 302
#         return redirect('home', permanent=True)  # постоянный редирект,
#         # редирект надо всегда возвращать, прямой адрес прописывать крайне не рекомендуется (хардкодинг)
#
#     return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


# Функция-представление для handler404
# Она будет вызываться каждый раз при возникновении исключения 404
# Можно определять обработчики для разных исключений:
# handler500 - ошибка сервера
# handler403 - доступ запрещен
# handler400 - невозможно обработать запрос
# все обработчики начинают работать только, когда DEBUG=False в settings.py проекта
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# создание 301 и 302 редиректов
# 301- страница перемещена на другой постоянный URL-адрес
# 302 - страница временно перемещена на другой URL-адрес
