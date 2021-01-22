from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.serializers import CustomUserSerializer, PostSerializer
from user.models import Post


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
	def test_get(self):
		User = get_user_model()
		user = User.objects.create_user(
			email='some@user.com', 
			password='password',
			first_name='John',
			last_name='Bath',
			hometown='Moscow',
			bio='Some time some text'
		)
		post_1 = Post.objects.create(
			author=user,
			content="Its content text 111111",
			title="title_post_1",
			created_on=None,
			updated_on=None
		)
		post_2 = Post.objects.create(
			author=user,
			content="Its content text 22222",
			title="title_post_2",
			created_on=None,
			updated_on=None
		)
		serializer_data = PostSerializer([post_1, post_2], many=True).data
		url = reverse('post-list')
		response = self.client.get(url)
		self.assertEqual(status.HTTP_200_OK, response.status_code)
		self.assertEqual(serializer_data, response.data)