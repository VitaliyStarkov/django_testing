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
            slug='note-slug',
            author=cls.author,
        )

    def test_note_in_list_for_author(self):
        url = reverse('notes:list')
        response = self.author.get(url)
        self.assertIn(self.note, response.context['object_list'])

    def test_note_not_in_list_for_another_user(self):
        url = reverse('notes:list')
        response = self.reader.get(url)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_create_note_page_contains_form(self):
        url = reverse('notes:add')
        response = self.client.get(url)
        self.assertIn('form', response.context)

    def test_edit_note_page_contains_form(self):
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertIn('form', response.context)
