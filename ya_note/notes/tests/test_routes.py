from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Артемка')
        cls.reader = User.objects.create(username='Кексик')
        cls.note = Note.objects.create(
            title='Новая заметка',
            text='Очень новая заметка',
            slug='SLUG ZAMETKI',
            author=cls.author
        )

    def test_pages_availability_for_different_users(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        urls = ('notes:list', 'notes:success', 'notes:add')
        for user, status in users_statuses:
            self.client.force_login(user)
            for page in urls:
                with self.subTest(user=user, page=page):
                    url = reverse(page, args=[self.note.slug])
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirects(self):
        urls = (
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:list', None),
            ('notes:success', None),
            ('notes:add', None),
        )
        for page, args in urls:
            with self.subTest(page=page):
                url = reverse(page, args=args)
                login_url = reverse('users:login')
                expected_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, expected_url)

    def test_pages_availability_for_anonymous_user(self):
        urls = ('users:login', 'users:logout', 'users:signup', 'notes:home')
        for page in urls:
            with self.subTest(page=page):
                url = reverse(page)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
