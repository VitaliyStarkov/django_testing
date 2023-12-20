import pytest
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Лев Толстой')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст'
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст'
    }


@pytest.fixture
def pk_for_com(comment):
    return comment.pk,


@pytest.fixture
def pk_for_news(news):
    return news.pk,


@pytest.fixture
def make_many_news():
    News.objects.bulk_create(
        News(title=f'News number {index}',
             text='News text',
             date=datetime.today() - timedelta(days=index)
             )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def make_2_com(author, news):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Text {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
