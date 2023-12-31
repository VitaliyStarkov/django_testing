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
            cls.url_home,
            cls.url_list,
            cls.url_detail,
            cls.url_edit,
            cls.url_delete,
            cls.url_success,
            cls.login_url,
            cls.url_add,
            cls.logout_url,
            cls.signup_url
        )
        cls.banned_urls_reader = (cls.url_detail,
                                  cls.url_edit,
                                  cls.url_delete)

    def test_all_urls_accessible_author(self):
        """Автору доступны все urls."""
        for url in self.cortege_urls:
            with self.subTest(url=url):
                res = self.author_client.get(url)
                self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_urls_for_auth_client(self):
        """Все urls кроме редактирования,
        удаления и детали доступны не автору.
        """
        banned_urls_reader = (self.url_detail,
                              self.url_edit,
                              self.url_delete)
        for url in self.cortege_urls:
            with self.subTest(url=url):
                res = self.reader_client.get(url)
                if url in banned_urls_reader:
                    self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)
                else:
                    self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_redirects(self):
        """Незарегистрированный пользователь
        переадресовывается на страницу регистрации.
        """
        banned_urls_client = (self.url_add,
                              self.url_success,
                              self.url_delete,
                              self.url_edit,
                              self.url_detail,
                              self.url_list)
        for url in self.cortege_urls:
            with self.subTest(url=url):
                res = self.client.get(url)
                if url in banned_urls_client:
                    expected_url = f'{self.login_url}?next={url}'
                    response = self.client.get(url)
                    self.assertRedirects(response, expected_url)
                else:
                    self.assertEqual(res.status_code, HTTPStatus.OK)
