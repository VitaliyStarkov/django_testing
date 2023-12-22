import pytest

from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, make_many_news, url_home):
    """Количество новостей на главной странице не более 10"""
    response = client.get(url_home)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, make_many_news, url_home):
    """Новости отсортированы от самой свежей к самой старой.
    Свежие новости в начале списка
    """
    response = client.get(url_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news, make_2_com, url_detail):
    """Комментарии на странице отдельной новости отсортированы
    в хронологическом порядке: старые в начале списка, новые — в конце
    """
    response = client.get(url_detail)
    list_comments = response.context['news'].comment_set.all()
    all_dates = [comment.created for comment in list_comments]
    sorted_dates = sorted(all_dates)
    assert all_dates == sorted_dates


@pytest.mark.parametrize(
    'clients, is_permitted', ((pytest.lazy_fixture('admin_client'), True),
                              (pytest.lazy_fixture('client'), False))
)
def test_comment_form_availability_for_different_users(
        news, clients, is_permitted, url_detail):
    """Зарегестрированный пользователь может оставить комментарий,
    незарегестрированный - нет
    """
    response = clients.get(url_detail)
    result = 'form' in response.context
    assert result == is_permitted


def test_for_author_in_form_there_commentform(admin_client, news, url_detail):
    """Зарегистрированному пользователю на страницу отдельной новости
    передаётся форма комментария
    """
    response = admin_client.get(url_detail)
    list_forms = response.context['form']
    assert isinstance(list_forms, CommentForm)
