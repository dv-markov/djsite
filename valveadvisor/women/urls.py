from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', WomenHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category')

    # path('', cache_page(60)(WomenHome.as_view()), name='home'),  # 1-й способ кэширования, через cache_page для класса
    # отображение по номеру категории вместо слага
    # path('category/<int:cat_id>/', show_category, name='category')

    # path('cats/<slug:cat>/', categories),  # http://127.0.0.1:8000/cats/<cat>
    # path('cats/<int:catid>/', categories),  # http://127.0.0.1:8000/cats/<catid>
    # формирование шаблона маршрута с помощью регулярного выражения
    # re_path(r"^archive/(?P<year>[0-9]{4})/", archive)
]

