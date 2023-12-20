import pytest
from django.urls import reverse
from django.conf import settings

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('make_many_news')
def test_news_count(client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('make_many_news')
def test_news_order(client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.usefixtures('make_2_com')
def test_comments_order(client, news):
    url = reverse('news:detail', args=[news.id,])
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created <= all_comments[1].created


@pytest.mark.parametrize(
    'username, is_permitted', ((pytest.lazy_fixture('admin_client'), True),
                               (pytest.lazy_fixture('client'), False))
)
def test_comment_form_availability_for_different_users(
        news, username, is_permitted):
    url = reverse('news:detail', args=(news.pk,))
    res = username.get(url)
    result = 'form' in res.context
    assert result == is_permitted
