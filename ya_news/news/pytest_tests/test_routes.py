import pytest
from http import HTTPStatus

from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, clients, status', ((lazy_fixture('url_detail'),
                              pytest.lazy_fixture('client'),
                              HTTPStatus.OK),
                             (lazy_fixture('url_home'),
                              pytest.lazy_fixture('client'),
                              HTTPStatus.OK),
                             (lazy_fixture('login_url'),
                              pytest.lazy_fixture('client'),
                              HTTPStatus.OK),
                             (lazy_fixture('logout_url'),
                              pytest.lazy_fixture('client'),
                              HTTPStatus.OK),
                             (lazy_fixture('signup_url'),
                              pytest.lazy_fixture('client'),
                              HTTPStatus.OK),
                             (lazy_fixture('url_edit'),
                              pytest.lazy_fixture('author_client'),
                              HTTPStatus.OK),
                             (lazy_fixture('url_edit'),
                              pytest.lazy_fixture('admin_client'),
                              HTTPStatus.NOT_FOUND),
                             (lazy_fixture('url_delete'),
                              pytest.lazy_fixture('author_client'),
                              HTTPStatus.OK),
                             (lazy_fixture('url_delete'),
                              pytest.lazy_fixture('admin_client'),
                              HTTPStatus.NOT_FOUND))
)
def test_pages_availability_for_certain_user(
    url, clients, status
):
    """Проверка доступа к страницам"""
    response = clients.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('url_delete'),
     pytest.lazy_fixture('url_edit')),
)
def test_redirects(client, url, login_url):
    """Незарегистрированный пользователь
    переадресовывается на страницу регистрации
    """
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
