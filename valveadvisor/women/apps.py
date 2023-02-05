from django.apps import AppConfig


# Класс для описания всего приложения в целом
class WomenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'
    verbose_name = 'Женщины мира'
