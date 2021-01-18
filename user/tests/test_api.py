from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.serializers import CustomUserSerializer


class CustomUserApiTestCase(APITestCase):
	def test_get(self):
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
		url = reverse('user-list')
		response = self.client.get(url)
		serializer_data = CustomUserSerializer([user_1, user_2], many=True).data
		self.assertEqual(status.HTTP_200_OK, response.status_code)
		# self.assertEqual(serializer_data, response.data)