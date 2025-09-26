from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post, PostTag, Type


class PostListViewTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		user_model = get_user_model()
		cls.user = user_model.objects.create_user(username='alice', password='password123')
		cls.type_cat = Type.objects.create(type_name='gatos')
		cls.type_dog = Type.objects.create(type_name='perros')

		cls.post_cat = Post.objects.create(post_content='Contenido sobre gatos', username=cls.user)
		PostTag.objects.create(post_id=cls.post_cat, type_id=cls.type_cat)

		cls.post_dog = Post.objects.create(post_content='Contenido sobre perros', username=cls.user)
		PostTag.objects.create(post_id=cls.post_dog, type_id=cls.type_dog)

	def setUp(self):
		self.client.force_login(self.user)

	def test_filter_by_type_parameter(self):
		response = self.client.get(reverse('blog-home'), {'type': 'gatos'})
		self.assertEqual(response.status_code, 200)

		posts = list(response.context['posts'])
		self.assertEqual(len(posts), 1)
		self.assertEqual(posts[0], self.post_cat)
		self.assertEqual(response.context['active_type'], 'gatos')

	def test_search_bar_type_case_insensitive(self):
		response = self.client.get(reverse('blog-home'), {'type': 'GATOS'})
		self.assertEqual(response.status_code, 200)

		posts = list(response.context['posts'])
		self.assertEqual(len(posts), 1)
		self.assertEqual(posts[0], self.post_cat)
		self.assertEqual(response.context['active_type'], 'gatos')

	def test_general_query_fallback(self):
		response = self.client.get(reverse('blog-home'), {'q': 'perros'})
		self.assertEqual(response.status_code, 200)

		posts = list(response.context['posts'])
		self.assertEqual(len(posts), 1)
		self.assertEqual(posts[0], self.post_dog)
		self.assertEqual(response.context['active_type'], 'perros')
