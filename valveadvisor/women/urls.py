from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index, name='home'),  # http://127.0.0.1:8000/
    path('about/', about, name='about'),
    path('addpage/', addpage, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login')

    # path('cats/<slug:cat>/', categories),  # http://127.0.0.1:8000/cats/<cat>
    # path('cats/<int:catid>/', categories),  # http://127.0.0.1:8000/cats/<catid>
    # re_path(r"^archive/(?P<year>[0-9]{4})/", archive),  # формирование шаблона маршрута с помощью регулярного выражения
]
