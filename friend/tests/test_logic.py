from django.test import TestCase
from django.contrib.auth import get_user_model
from friend.models import FriendList


class FriendListTestCase(TestCase):
	def setUp(self):
		User = get_user_model()
		self.sender_1 = User.objects.create_user(
			email='sender_1@mail.com', 
			password='password',
			first_name='sender1_name',
			last_name='sender1_lname',
			hometown='Moscow',
			bio='bio sender_1'
		)
		self.receiver_1 = User.objects.create_user(
			email='receiver_1@mail.com', 
			password='password',
			first_name='receiver1_name',
			last_name='receiver1_lname',
			hometown='Moscow',
			bio='bio receiver_1'
		)

	def test_create_friendlist(self):
		FriendList.objects.create(user=self.sender_1)
		friend_list = FriendList.objects.get(user=self.sender_1)
		self.assertTrue(friend_list)

	def test_add_friend(self):
		FriendList.objects.create(user=self.sender_1)
		sender_friend_list = FriendList.objects.get(user=self.sender_1)
		sender_friend_list.add_friend(self.receiver_1)
		if self.receiver_1 not in sender_friend_list.friends.all():
				raise ValueError(f'{self.receiver_1.first_name} is not your friend')
		

	def test_remove_friend(self):
		FriendList.objects.create(user=self.sender_1)
		sender_friend_list = FriendList.objects.get(user=self.sender_1)
		sender_friend_list.add_friend(self.receiver_1)
		sender_friend_list.remove_friend(self.receiver_1)
		if self.receiver_1 in sender_friend_list.friends.all():
				raise ValueError(f'{self.receiver_1.first_name} has not been removed')


	def unfriend(self):
		pass