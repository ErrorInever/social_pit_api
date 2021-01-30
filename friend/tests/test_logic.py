from django.test import TestCase
from django.contrib.auth import get_user_model
from friend.models import FriendList, FriendRequest
from django.core.exceptions import ValidationError
from friend.exceptions import AlreadyFriendsError, FriendListsDoesNotExist


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
		"""
		Trying to create a friendlist object
		"""
		FriendList.objects.create(user=self.sender_1)
		friend_list = FriendList.objects.get(user=self.sender_1)
		self.assertTrue(friend_list)


	def test_add_friend(self):
		"""
		'Sender' trying to add 'receiver' in his friendlist
		"""
		FriendList.objects.create(user=self.sender_1)
		sender_friend_list = FriendList.objects.get(user=self.sender_1)
		sender_friend_list.add_friend(self.receiver_1)
		if self.receiver_1 not in sender_friend_list.friends.all():
				raise ValueError(f'{self.receiver_1.first_name} is not your friend')


	def test_add_friend_yourself(self):
		FriendList.objects.create(user=self.sender_1)
		sender_friend_list = FriendList.objects.get(user=self.sender_1)
		with self.assertRaises(ValidationError) as e:
			sender_friend_list.add_friend(self.sender_1)


	def test_add_friend_if_users_already_friends(self):
		FriendList.objects.create(user=self.sender_1)
		sender_friend_list = FriendList.objects.get(user=self.sender_1)
		sender_friend_list.add_friend(self.receiver_1)
		with self.assertRaises(AlreadyFriendsError) as e:
			sender_friend_list.add_friend(self.receiver_1)


	def test_remove_friend(self):
		FriendList.objects.create(user=self.sender_1)
		sender_friend_list = FriendList.objects.get(user=self.sender_1)
		sender_friend_list.add_friend(self.receiver_1)

		self.assertTrue(sender_friend_list.remove_friend(self.receiver_1))
		self.assertFalse(sender_friend_list.remove_friend(self.sender_1))

		if self.receiver_1 in sender_friend_list.friends.all():
				raise ValueError(f'{self.receiver_1.first_name} has not been removed!')


	def test_unfriend(self):
		"""
		Trying to initiate the action of unfriending.
		"""
		FriendList.objects.create(user=self.sender_1)
		FriendList.objects.create(user=self.receiver_1)
		sender_friend_list = FriendList.objects.get(user=self.sender_1)
		receiver_friend_list = FriendList.objects.get(user=self.receiver_1)

		sender_friend_list.add_friend(self.receiver_1)
		receiver_friend_list.add_friend(self.sender_1)

		sender_friend_list.unfriend(self.receiver_1)

		if (self.receiver_1 in sender_friend_list.friends.all() or 
				self.sender_1 in receiver_friend_list.friends.all()):
			raise ValueError(f'{self.receiver_1} and {self.sender_1} has not been unfriended!')


	def test_unfriend_negative(self):
		"""
		Trying to initiate the action of unfriending if users are not friends
		"""
		FriendList.objects.create(user=self.sender_1)
		sender_friend_list = FriendList.objects.get(user=self.sender_1)
		with self.assertRaises(ValidationError) as e:
			sender_friend_list.unfriend(self.receiver_1)



class FriendRequestTestCase(TestCase):
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


	def test_accept_request(self):
		friend_request = FriendRequest.objects.create(sender=self.sender_1, receiver=self.receiver_1, is_active=True)
		friend_request.accept()

		sender_friend_list = FriendList.objects.get(user=self.sender_1)
		receiver_friend_list = FriendList.objects.get(user=self.receiver_1)

		self.assertTrue(sender_friend_list.is_mutual_friend(self.receiver_1))
		self.assertTrue(receiver_friend_list.is_mutual_friend(self.sender_1))


	def test_accept_request_negative(self):
		friend_request = FriendRequest.objects.create(sender=self.sender_1, receiver=self.receiver_1, is_active=False)
		
		with self.assertRaises(ValidationError) as e:
			friend_request.accept()


	def test_decline_request(self):
		friend_request = FriendRequest.objects.create(sender=self.sender_1, receiver=self.receiver_1, is_active=True)
		self.assertTrue(friend_request.is_active)
		friend_request.decline()
		self.assertFalse(friend_request.is_active)


	def test_cancel_request(self):
		friend_request = FriendRequest.objects.create(sender=self.sender_1, receiver=self.receiver_1, is_active=True)
		self.assertTrue(friend_request.is_active)
		friend_request.cancel()
		self.assertFalse(friend_request.is_active)
