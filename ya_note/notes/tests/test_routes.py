from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Новая заметка',
            text='Очень новая заметка',
            slug='note-slug',
            author=cls.author
        )
        cls.slug = [cls.note.slug]
        cls.url_home = reverse('notes:home')
        cls.url_list = reverse('notes:list')
        cls.url_detail = reverse('notes:detail', args=cls.slug)
        cls.url_edit = reverse('notes:edit', args=cls.slug)
        cls.url_delete = reverse('notes:delete', args=cls.slug)
        cls.url_success = reverse('notes:success')
        cls.login_url = reverse('users:login')
        cls.url_add = reverse('notes:add')
        cls.logout_url = reverse('users:logout')
        cls.signup_url = reverse('users:signup')
        cls.cortege_urls = (
            (cls.url_home, HTTPStatus.OK, HTTPStatus.OK),
            (cls.url_list, HTTPStatus.OK, HTTPStatus.FOUND),
            (cls.url_detail, HTTPStatus.NOT_FOUND, HTTPStatus.FOUND),
            (cls.url_edit, HTTPStatus.NOT_FOUND, HTTPStatus.FOUND),
            (cls.url_delete, HTTPStatus.NOT_FOUND, HTTPStatus.FOUND),
            (cls.url_success, HTTPStatus.OK, HTTPStatus.FOUND),
            (cls.login_url, HTTPStatus.OK, HTTPStatus.OK),
            (cls.url_add, HTTPStatus.OK, HTTPStatus.FOUND),
            (cls.logout_url, HTTPStatus.OK, HTTPStatus.OK),
            (cls.signup_url, HTTPStatus.OK, HTTPStatus.OK)
        )

    def test_all_urls_accessible_author(self):
        """
        Автору доступны все urls
        """
        for url, status, status_for_anonymous in self.cortege_urls:
            with self.subTest(url=url):
                res = self.author_client.get(url)
                self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_urls_for_auth_client(self):
        """
        Все urls кроме редактирования,
        удаления и детали доступны не автору
        """
        for url, status, status_for_anonymous in self.cortege_urls:
            with self.subTest(url=url, status=status):
                res = self.reader_client.get(url)
                self.assertEqual(res.status_code, status)

    def test_redirects(self):
        """
        Незарегистрированный пользователь
        переадресовывается на страницу регистрации
        """
        for url, status, status_for_anonymous in self.cortege_urls:
            with self.subTest(
                url=url,
                status_for_anonymous=status_for_anonymous
            ):
                res = self.client.get(url)
                self.assertEqual(res.status_code, status_for_anonymous)
