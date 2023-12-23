import pytest

from http import HTTPStatus

from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

pytestmark = pytest.mark.django_db

url_detail = lazy_fixture('url_detail')
url_home = lazy_fixture('url_home')
login_url = lazy_fixture('login_url')
logout_url = lazy_fixture('logout_url')
signup_url = lazy_fixture('signup_url')
url_edit = lazy_fixture('url_edit')
url_delete = lazy_fixture('url_delete')
client = pytest.lazy_fixture('client')
author_client = pytest.lazy_fixture('author_client')
admin_client = pytest.lazy_fixture('admin_client')


@pytest.mark.parametrize(
    'url, clients, status', ((url_detail,
                              client,
                              HTTPStatus.OK),
                             (url_home,
                              client,
                              HTTPStatus.OK),
                             (login_url,
                              client,
                              HTTPStatus.OK),
                             (logout_url,
                              client,
                              HTTPStatus.OK),
                             (signup_url,
                              client,
                              HTTPStatus.OK),
                             (url_edit,
                              author_client,
                              HTTPStatus.OK),
                             (url_edit,
                              admin_client,
                              HTTPStatus.NOT_FOUND),
                             (url_delete,
                              author_client,
                              HTTPStatus.OK),
                             (url_delete,
                              admin_client,
                              HTTPStatus.NOT_FOUND))
)
def test_pages_availability_for_certain_user(
    url, clients, status
):
    """Проверка доступа к страницам."""
    response = clients.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'url',
    (url_delete, url_edit),
)
def test_redirects(client, url, login_url):
    """Незарегистрированный пользователь
    переадресовывается на страницу регистрации.
    """
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
