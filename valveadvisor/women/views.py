from django.contrib.auth import logout, login
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import AuthenticationForm
# from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
# render - встроенный шаблонизатор Django
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

from .forms import *
from .models import *
from .utils import *


# Представление главной страницы в виде функции
# def index(request):  # HttpRequest
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': "Главная страница",
#         'cat_selected': 0
#     }
#     return render(request, 'women/index.html', context=context)


# Представление главной страницы в виде класса ListView
# class WomenHome(ListView):
#     model = Women
#     template_name = 'women/index.html'
#     context_object_name = 'posts'
#     # параметр для передачи статических (неизменяемых) значений, не подходит для списков
#     # extra_context = {'title': 'Главная страница'}
#
#     # второй вариант передачи дополнительных данных в шаблон - функция get_context_data
#     def get_context_data(self, *, object_list=None, **kwargs):
#         # сначала получаем текущий контекст
#         context = super().get_context_data(**kwargs)
#         context['menu'] = menu
#         context['title'] = 'Главная страница'
#         context['cat_selected'] = 0
#         return context
#
#     def get_queryset(self):
#         return Women.objects.filter(is_published=True)


# Использование миксинов
class WomenHome(DataMixin, ListView):
    # переменная пагинатора для указания количества элементов на одной странице, перенесена в DataMixin
    # paginate_by = 3
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # параметр для передачи статических (неизменяемых) значений, не подходит для списков
    # extra_context = {'title': 'Главная страница'}

    # второй вариант передачи дополнительных данных в шаблон - функция get_context_data
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        # return dict(list(context.items()) + list(c_def.items()))
        return context | c_def

    def get_queryset(self):
        # select_related - "жадный" запрос для внешнего ключа One-To-Many
        return Women.objects.filter(is_published=True).select_related('cat')


# @login_required # для функций представления используются декораторы, для классов - миксины
# def about(request):
#     # Класс Paginator в функциях-представлениях
#     # contact_list = Women.objects.all()
#     # paginator = Paginator(contact_list, 3)
#     #
#     # page_number = request.GET.get('page')
#     # page_obj = paginator.get_page(page_number)
#     #
#     # return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})
#
#     return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


class AboutSite(DataMixin, TemplateView):
    template_name = 'women/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="О сайте", cat_selected=None)
        return context | c_def


# Функция
# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#
#             # добавление данных с формы в базу, для форм не связанных с моделью
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#
#             # добавление данных в базу для форм, связанных с моделью
#             # ошибки обрабатываются автоматически
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': "Добавление статьи"})


# Класс CreateView
# class AddPage(CreateView):
#     form_class = AddPostForm
#     template_name = 'women/addpage.html'
#     # адрес для перенаправления после создания
#     success_url = reverse_lazy('home')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Добавление статьи'
#         context['menu'] = menu
#         return context


# Миксин
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # адрес для перенаправления после создания
    success_url = reverse_lazy('home')
    # login_url = '/admin/'
    login_url = reverse_lazy('home')
    raise_exception = True  # отображение 403 вместо перенаправления

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи', cat_selected=None)
        # return dict(list(context.items()) + list(c_def.items()))
        return context | c_def


# def contact(request):
#     return HttpResponse("Обратная связь")


# FormView - стандартный базовый класс для форм, не привязанных к модели
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return context | c_def

    def form_valid(self, form):
        print(form.cleaned_data)
        # send_mail('Тема сообщения',
        #           'Содержание',
        #           'basmuleb@gmail.com',
        #           ['dmitry.v.markov@gmail.com']
        #           )
        return redirect('home')


# обработка представления через функцию
# def show_post(request, post_slug):
#     # return HttpResponse(f"Отображение статьи с id = {post_id}")
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


# Обработка представления через DetailView
# class ShowPost(DetailView):
#     model = Women
#     template_name = 'women/post.html'
#     # замена стандартного пути обращения к слагу ('slug') на тот, который прописан в маршруте ('post_slug')
#     slug_url_kwarg = 'post_slug'
#     # имя специальной переменной для замены пути обращения по id, значение по умолчанию 'pk'
#     # pk_url_kwarg = 'pk'
#     context_object_name = 'post'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = context['post']
#         context['menu'] = menu
#         return context


# Обработка представления через миксин
class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    # замена стандартного пути обращения к слагу ('slug') на тот, который прописан в маршруте ('post_slug')
    # имя специальной переменной для замены пути обращения по id, значение по умолчанию 'pk'
    # pk_url_kwarg = 'pk'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'], cat_selected=None)
        return context | c_def

# отображение через функцию
# def show_category(request, cat_slug):
#     cat = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.objects.filter(cat_id=cat.pk)
#
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': f"Отображение рубрики {cat}",
#         'cat_selected': cat.pk
#     }
#
#     return render(request, 'women/index.html', context=context)


# отображение через класс
# class WomenCategory(ListView):
#     model = Women
#     template_name = 'women/index.html'
#     context_object_name = 'posts'
#     allow_empty = False
#
#     def get_queryset(self):
#         return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Категория - ' + str(context['posts'][0].cat)
#         context['menu'] = menu
#         context['cat_selected'] = context['posts'][0].cat_id
#         return context


# Отображение с использованием миксина
class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        # select_related - "жадный" запрос для внешнего ключа One-To-Many
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
        #                               cat_selected=context['posts'][0].cat_id)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return context | c_def


# пример простейшей реализации представления
# def categories(request, catid):
#     if request.GET:
#         print(request.GET)
#     # if request.POST:
#     #     print(request.POST)
#
#     return HttpResponse(f"<h1>Статья по категориям</h1><p>{catid}</p>")


# Обработка ошибок вызова несуществующих страниц
# def archive(request, year):
#     if int(year) > 2022:
#         # raise Http404()
#         # return redirect('/')  # временный редирект для перенаправления с кодом 302
#         return redirect('home', permanent=True)  # постоянный редирект,
#         # редирект надо всегда возвращать, прямой адрес прописывать крайне не рекомендуется (хардкодинг)
#
#     return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")
#
#
# Функция-представление для handler404
# Она будет вызываться каждый раз при возникновении исключения 404
# Можно определять обработчики для разных исключений:
# handler500 - ошибка сервера
# handler403 - доступ запрещен
# handler400 - невозможно обработать запрос
# создание 301 и 302 редиректов
# 301- страница перемещена на другой постоянный URL-адрес
# 302 - страница временно перемещена на другой URL-адрес
# все обработчики начинают работать только, когда DEBUG=False в settings.py проекта
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(DataMixin, CreateView):
    # стандартная форма
    # form_class = UserCreationForm
    # пользовательская форма
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context | c_def

    # метод вызывается при успешной проверке формы регистрации
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


# def login(request):
#     return HttpResponse("Авторизация")


class LoginUser(DataMixin, LoginView):
    # стандартная форма авторизации
    # form_class = AuthenticationForm
    # пользовательская форма авторизации
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return context | c_def

    # метод вызывается, если пользователь успешно прошел авторизацию
    # альтернативный метод - константа LOGIN_REDIRECT_URL в settings.py
    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
