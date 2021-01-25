from django.test import TestCase
from user.serializers import CustomUserSerializer, PostSerializer
from django.contrib.auth import get_user_model
from user.models import Post, UserPostRelation
from django.db.models import Count, Case, When, Avg
from rest_framework import serializers


class CustomUserSerializerTestCase(TestCase):
	def _ok(self):
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
		data = CustomUserSerializer(user_1).data
		expected_data = [
			{
				'id': user_1.id,
				'password': user_1.password,
				'first_name': 'John',
				'last_name': 'Smith',
				'hometown': 'Moscow',
				'bio': 'Im some user this portal'
			}
		]


class PostSerializerTestCase(TestCase):
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

	def test_ok(self):
		posts = Post.objects.filter(id=self.post_1.id).annotate(
			annotated_likes=Count(Case(When(userpostrelation__like=True, then=1))),
			rating=Avg('userpostrelation__rate')
			)
		data = PostSerializer(posts, many=True).data
		expected_data = [{
				'id': self.post_1.id,
				'author': self.user_1.id,
				'content': "content text 11111",
				'title': "title_post_1",
				'created_on': serializers.DateTimeField().to_representation(self.post_1.created_on),
				'updated_on': serializers.DateTimeField().to_representation(self.post_1.updated_on),
				'annotated_likes': 0,
				'rating': None
			}]
		self.assertEqual(expected_data, data)

	def test_annotate(self):
		"""annotate each post and calculate likes"""
		UserPostRelation.objects.create(user=self.user_1, post=self.post_1, like=True, rate=3)
		UserPostRelation.objects.create(user=self.user_2, post=self.post_1, like=True, rate=4)
		posts = Post.objects.filter(id=self.post_1.id).annotate(
			annotated_likes=Count(Case(When(userpostrelation__like=True, then=1))),
			rating=Avg('userpostrelation__rate')
			).order_by('id')
		data = PostSerializer(posts, many=True).data
		expected_data = [{
				'id': self.post_1.id,
				'author': self.user_1.id,
				'content': "content text 11111",
				'title': "title_post_1",
				'created_on': serializers.DateTimeField().to_representation(self.post_1.created_on),
				'updated_on': serializers.DateTimeField().to_representation(self.post_1.updated_on),
				'annotated_likes': 2,
				'rating': '3.50'
			}]
		self.assertEqual(expected_data, data)
