from django.test import TestCase
from user.serializers import CustomUserSerializer, PostSerializer
from django.contrib.auth import get_user_model
from user.models import Post


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
	def test_ok(self):
		User = get_user_model()
		user = User.objects.create_user(
			email='some@user.com', 
			password='password',
			first_name='John',
			last_name='Bath',
			hometown='Moscow',
			bio='Some time some text'
		)
		post_1 = Post(
			author=user,
			content="Its content text 111111",
			title="title_1",
			created_on=None,
			updated_on=None
		)

		data = PostSerializer(post_1).data
		expected_data = {
				'id': post_1.id,
				'author': user.id,
				'content': "Its content text 111111",
				'title': 'title_1',
				'created_on': None,
				'updated_on': None
			}
		self.assertEqual(expected_data, data)