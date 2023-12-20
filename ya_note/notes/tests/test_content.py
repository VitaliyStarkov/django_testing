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
        self.client.force_login(self.author)
        url = reverse('notes:list')
        response = self.author.get(url)
        note_in_object_list = self.note in response.context['object_list']
        self.assertEqual(note_in_object_list, True)

    def test_note_not_in_list_for_another_user(self):
        self.client.force_login(self.reader)
        url = reverse('notes:list')
        response = self.reader.get(url)
        note_in_object_list = self.note in response.context['object_list']
        self.assertEqual(note_in_object_list, False)

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
