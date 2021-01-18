from rest_framework.test import APITestCase
from django.urls import reverse

class CustomUserApiTestCase(APITestCase):
	def test_get(self):
		url = reverse('user-list')
		print(url)
		response = self.client.get(url)
		print(response)