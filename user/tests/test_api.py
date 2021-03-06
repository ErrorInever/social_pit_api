import json
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.serializers import CustomUserSerializer, PostSerializer
from user.models import Post, UserPostRelation
from rest_framework import serializers
from django.db.models import Count, Case, When, Avg
from django.test.utils import CaptureQueriesContext
from django.db import connection


class CustomUserApiTestCase(APITestCase):
	def _get(self):
		User = get_user_model()
		user_1 = User.objects.create_user(
			email='some@mail.ru',
			password='123456',
			first_name='John',
			last_name = 'Smith',
			hometown='Moscow',
			bio = 'Im some user this portal'
		)
		user_2 = User.objects.create_user(
			email='some1@mail.ru',
			password='123456',
			first_name='Jan',
			last_name = 'Pere',
			hometown='Paris',
			bio = 'Im a human'
		)
		url = reverse('users-list')
		response = self.client.get(url)
		serializer_data = CustomUserSerializer([user_1, user_2], many=True).data
		self.assertEqual(status.HTTP_200_OK, response.status_code)
		# self.assertEqual(serializer_data, response.data)


class PostApiTestCase(APITestCase):
	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(
			email='some@user.com', 
			password='password',
			first_name='John',
			last_name='Bath',
			hometown='Moscow',
			bio='Some time some text'
		)
		self.user_2 = User.objects.create_user(
			email='some2@user.com', 
			password='password2',
			first_name='Boby',
			last_name='GBr',
			hometown='SPB',
			bio='Some 123211221'
		)
		self.staff_user = User.objects.create_user(
			email='staff@mail.ru',
			password='123456',
			first_name='Robert',
			last_name = 'Pure',
			hometown='Egypt',
			bio = 'Im a machine',
			is_staff=True
		)
		self.post_1 = Post.objects.create(
			author=self.user,
			content="1111111",
			title="title_post_1",
			created_on=None,
			updated_on=None
		)
		self.post_2 = Post.objects.create(
			author=self.user_2,
			content="2222222",
			title="title_post_2",
			created_on=None,
			updated_on=None
		)

	def test_get(self):
		posts = Post.objects.all().annotate(
			annotated_likes=Count(Case(When(userpostrelation__like=True, then=1))))
		serializer_data = PostSerializer(posts, many=True).data
		url = reverse('post-list')
		with CaptureQueriesContext(connection) as queries:
			# test SQL queries select_related and prefetch_related
			response = self.client.get(url)
			self.assertEqual(2, len(queries), 'SQL queries not optimize')

		self.assertEqual(status.HTTP_200_OK, response.status_code)
		self.assertEqual(serializer_data, response.data)

	def test_create(self):
		self.assertEqual(2, Post.objects.all().count())
		url = reverse('post-list')
		data = {
			"author": 1,
			"content": "Test text content",
			"title": "some title"
		}
		json_data = json.dumps(data)
		self.client.force_login(self.user)
		response = self.client.post(url, data=json_data, content_type='application/json')
		self.assertEqual(3, Post.objects.all().count())

		self.assertEqual(status.HTTP_201_CREATED, response.status_code)
		self.assertEqual(self.user, Post.objects.last().author)	

	def test_update(self):
		url = reverse('post-detail', args=(self.post_1.id,))
		data = {
			"author": self.user.id,
			"content": self.post_1.content,
			"title": "new title"
		}
		json_data = json.dumps(data)
		self.client.force_login(self.user)
		response = self.client.put(url, data=json_data, content_type='application/json')
		self.assertEqual(status.HTTP_200_OK, response.status_code)
		#self.post_1 = Post.objects.get(id=self.post_1.id)
		self.post_1.refresh_from_db()
		self.assertEqual("new title", self.post_1.title)


	def test_update_not_author(self):
		url = reverse('post-detail', args=(self.post_2.id,))
		data = {
			"author": self.user_2.id,
			"content": self.post_2.content,
			"title": "new title"
		}
		json_data = json.dumps(data)
		self.client.force_login(self.user)
		response = self.client.put(url, data=json_data, content_type='application/json')
		self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
		#self.post_1 = Post.objects.get(id=self.post_1.id)
		self.post_1.refresh_from_db()
		self.assertEqual("title_post_2", self.post_2.title)

	def test_update_not_author_but_staff(self):
		url = reverse('post-detail', args=(self.post_2.id,))
		data = {
			"author": self.user_2.id,
			"content": self.post_2.content,
			"title": "new title"
		}
		json_data = json.dumps(data)
		self.client.force_login(self.staff_user)
		response = self.client.put(url, data=json_data, content_type='application/json')
		self.assertEqual(status.HTTP_200_OK, response.status_code)
		self.post_2.refresh_from_db()
		self.assertEqual("new title", self.post_2.title)


	def test_read(self):
		url = reverse('post-detail', args=(self.post_1.id,))
		response = self.client.get(url)
		expected_data = {
				'id': self.post_1.id,
				'author': self.user.id,
				'content': self.post_1.content,
				'title': self.post_1.title,
				'created_on': serializers.DateTimeField().to_representation(self.post_1.created_on),
				'updated_on': serializers.DateTimeField().to_representation(self.post_1.updated_on),
				'annotated_likes': 0,
				'rating': None,
				'owner_name': 'John',
				'post_reader': []
			}
		self.assertEqual(expected_data, response.data)


	def test_delete(self):
		self.client.force_login(self.user)
		url = reverse('post-detail', args=(self.post_1.id,))
		response = self.client.delete(url)
		self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
		response = self.client.delete(url)
		self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class UserPostRelationApiTestCase(APITestCase):
	def setUp(self):
		User = get_user_model()
		self.user_1 = User.objects.create_user(
			email='user_1@mail.com', 
			password='password',
			first_name='user_1',
			last_name='user_1',
			hometown='Moscow',
			bio='Some time user_1'
		)
		self.user_2 = User.objects.create_user(
			email='user_2@mail.com', 
			password='password',
			first_name='user_2',
			last_name='user_2',
			hometown='SPB',
			bio='Some time user_2'
		)
		self.post_1 = Post.objects.create(
			author=self.user_1,
			content="content text 11111",
			title="title_post_1",
			created_on=None,
			updated_on=None
		)
		self.post_2 = Post.objects.create(
			author=self.user_2,
			content="content text 22222",
			title="title_post_2",
			created_on=None,
			updated_on=None
		)

	def test_like(self):
		url = reverse('post_relation-detail', args=(self.post_1.id,))

		data = {
			"like": True,
		}

		json_data = json.dumps(data)
		self.client.force_login(self.user_1)
		response = self.client.patch(url, data=json_data, content_type='application/json')
		relation = UserPostRelation.objects.get(user=self.user_1.id, post=self.post_1)
		self.assertTrue(relation.like)
		self.assertEqual(status.HTTP_200_OK, response.status_code)