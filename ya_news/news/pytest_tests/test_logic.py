import pytest

from http import HTTPStatus
from random import choice

from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_author_can_edit_comment(author_client, form_data, comment, news):
    url = reverse('news:edit', args=[comment.pk])
    response = author_client.post(url, data=form_data)
    expected_url = reverse('news:detail', args=(news.pk,)) + '#comments'
    assertRedirects(response, expected_url)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_other_user_cant_edit_comment(admin_client, form_data, comment):
    url = reverse('news:edit', args=[comment.pk])
    response = admin_client.post(url, form_data)
    old_com = comment.text
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == old_com


def test_author_can_delete_comment(author_client, pk_for_com, news):
    url = reverse('news:delete', args=pk_for_com)
    response = author_client.post(url)
    expected_url = reverse('news:detail', args=(news.pk,)) + '#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_comment(admin_client, news, pk_for_com):
    url = reverse('news:delete', args=pk_for_com)
    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_user_can_create_comment(admin_client, news, form_data):
    url = reverse('news:detail', args=[news.pk])
    response = admin_client.post(url, data=form_data)
    expected_url = url + '#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_other_user_cant_create_comment(client, news, form_data):
    url = reverse('news:detail', args=[news.pk])
    response = client.post(url, data=form_data)
    assert Comment.objects.count() == 0


def test_user_cant_use_bad_words(admin_client, news):
    bad_words_data = {'text': f'Mr Petrov {choice(BAD_WORDS)}!'}
    url = reverse('news:detail', args=[news.pk])
    response = admin_client.post(url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == 0
