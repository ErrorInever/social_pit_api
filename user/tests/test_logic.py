from django.test import TestCase
from django.contrib.auth import get_user_model
from user.models import Post, UserPostRelation
from user.logic import set_rating


class SetRatingTestCase(TestCase):
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
		self.post_1 = Post.objects.create(
			author=self.user_1,
			content="content text 11111",
			title="title_post_1",
			created_on=None,
			updated_on=None
		)
		UserPostRelation.objects.create(user=self.user_1, 
										post=self.post_1, 
										like=True, 
										rate=3)

	def test_ok(self):
		set_rating(self.post_1)
		self.post_1.refresh_from_db()
		self.assertEqual('3.00', str(self.post_1.rating))


class UsersManagersTests(TestCase):

	def test_create_user(self):
		User = get_user_model()
		user = User.objects.create_user(
			email='some@user.com', 
			password='password',
			first_name='John',
			last_name='Bath',
			hometown='Moscow',
			bio='Some time some text'
		)
		self.assertEqual(user.email, 'some@user.com')
		self.assertEqual(user.first_name, 'John')
		self.assertEqual(user.last_name, 'Bath')
		self.assertEqual(user.hometown, 'Moscow')
		self.assertEqual(user.bio, 'Some time some text')
		self.assertEqual(user.__str__(), user.email)
		self.assertTrue(user.is_active)
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)
		try:
			self.assertIsNone(user.username)
		except AttributeError:
			pass
		with self.assertRaises(TypeError):
			User.objects.create_user()
		# with self.assertRaises(TypeError):
		# 	User.objects.create_user(email='')
		# with self.assertRaises(TypeError):
		# 	User.objects.create_user(email='', password='password')

	def test_create_superuser(self):
		User = get_user_model()
		admin_user = User.objects.create_superuser('super@user.com', 'password')
		self.assertEqual(admin_user.email, 'super@user.com')
		self.assertTrue(admin_user.is_active)
		self.assertTrue(admin_user.is_staff)
		self.assertTrue(admin_user.is_superuser)
		try:
			self.assertIsNone(admin_user.username)
		except AttributeError:
			pass
		with self.assertRaises(ValueError):
			User.objects.create_superuser(
				email='super@user.com', password='password', is_superuser=False
				)


class PostTests(TestCase):

	def test_create_post(self):
		User = get_user_model()
		user = User.objects.create_user(
			email='some@user.com', 
			password='password',
			first_name='John',
			last_name='Bath',
			hometown='Moscow',
			bio='Some time some text'
		)
		post = Post.objects.create(
			author=user,
			content="Its content text",
			title="title_post"
		)
		self.assertEqual(user, post.author)
		self.assertEqual("Its content text", post.content)
		self.assertEqual("title_post", post.title)
		self.assertEqual("title_post", post.__str__())


