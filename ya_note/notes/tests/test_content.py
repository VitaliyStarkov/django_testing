from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Артемка')
        cls.reader = User.objects.create(username='Кексик')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='slug заметки',
            author=cls.author,
        )

    def test_notes_list_for_different_users(self):
        users_notes = (
            (self.author, True),
            (self.reader, False),
        )
        url = reverse('notes:list')
        for user, true_or_false in users_notes:
            self.client.force_login(user)
            with self.subTest(user=user.username, true_or_false=true_or_false):
                response = self.client.get(url)
                note_in_object_list = self.note in response.context[
                    'object_list'
                ]
                self.assertEqual(note_in_object_list, true_or_false)

    def test_create_note_page_contains_form(self):
        self.client.force_login(self.author)
        url = reverse('notes:add')
        response = self.client.get(url)
        self.assertIn('form', response.context)

    def test_edit_note_page_contains_form(self):
        self.client.force_login(self.author)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertIn('form', response.context)
