from sqladmin import ModelView
from app.models.url import Url

class UrlAdmin(ModelView, model=Url):
    # Какие колонки отображать в списке
    column_list = ["id", "short_code", "url"]

    # По каким полям работает поиск
    column_searchable_list = ["url"]

    column_formatters = {
        # m — это объект модели (запись из базы)
        # a — это атрибут (название колонки)
        "url": lambda m, a: m.url[:50] + "..." if len(m.url) > 50 else m.url
    }

    column_sortable_list = ["id", "short_code", "url"]

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True

    page_size = 25
    page_size_options = [25, 50, 100, 200]