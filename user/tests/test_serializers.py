from django.test import TestCase
from user.serializers import CustomUserSerializer
from django.contrib.auth import get_user_model


class CustomUserSerializerTestCase(TestCase):
	def test_ok(self):
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
		self.assertEqual(expected_data, data)