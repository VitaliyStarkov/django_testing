from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )
        cls.url_list = reverse('notes:list')
        cls.url_add = reverse('notes:add')
        cls.url_edit = reverse('notes:edit', args=(cls.note.slug,))

    def test_notes_list_for_reader_users(self):
        """
        В список заметок одного пользователя
        не попадают заметки другого пользователя
        """
        count_initial = Note.objects.filter(author=self.author).count()
        response = self.author_client.get(self.url_list)
        object_list = response.context['object_list']

        self.assertEqual(len(object_list), count_initial)

    def test_notes_list_for_author_users(self):
        """
        У автора заметки есть заметка в списке
        """
        response = self.author_client.get(self.url_list)
        object_list = response.context['object_list']
        note = object_list.get(pk=self.note.pk)
        self.assertIn(self.note, object_list)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_form_in_create_edit_pages(self):
        """
        На страницах создания и редактирования заметки передаются формы
        """
        for url in (self.url_add, self.url_edit):
            with self.subTest(url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                list_forms = response.context['form']
                self.assertIsInstance(list_forms, NoteForm)
