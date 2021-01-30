from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from friend.exceptions import AlreadyFriendsError, FriendListsDoesNotExist


class FriendList(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
	friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')


	def __str__(self):
		return f'{self.user.first_name}{self.user.first_name}'


	def add_friend(self, account):
		"""
		Add a new friend
		"""
		if self.user == account:
			raise ValidationError('Users cannot be friends with themselves')

		if not account in self.friends.all():
			self.friends.add(account)
		else:
			raise AlreadyFriendsError('Sender and receiver are already friends')

		# TODO add if friendship already requested


	def remove_friend(self, account):
		"""
		Remove a friend
		"""
		if account in self.friends.all():
			self.friends.remove(account)
			return True
		else:
			return False


	def unfriend(self, removee):
		"""
		Initiate the action of unfriending someone.
		"""
		if self.user == removee:
			raise ValidationError('Users cannot unfriend with themselves')

		remover_friends_list = self # person terminating the friendship

		# Remove friend from remover friend list
		if self.is_mutual_friend(removee):
			remover_friends_list.remove_friend(removee)
		else:
			raise ValidationError('cannot unfriend if user is not friend')


		# Remove friend from removee friend list
		try:
			friends_list = FriendList.objects.get(user=removee)
		except ObjectDoesNotExist:
			raise FriendListsDoesNotExist('removee friendlist still not created')

		friends_list.remove_friend(self.user)


	def is_mutual_friend(self, friend):
		"""
		Is this a friend?
		"""
		if friend in self.friends.all():
			return True
		else:
			return False


class FriendRequest(models.Model):
	"""
	A friend request
	"""
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
	is_active = models.BooleanField(blank=True, null=True, default=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.sender.first_name}{self.sender.first_name}'


	def accept(self):
		"""
		Accept a friend request
		Update both SENDER and RECEIVER friend list
		"""
		receiver_friend_list = FriendList.objects.get(user=self.receiver)
		if receiver_friend_list:
			receiver_friend_list.add_friend(self.sender)
			sender_friend_list = FriendList.objects.get(user=self.sender)
			if sender_friend_list:
				sender_friend_list.add_friend(self.receiver)
				self.is_active = False
				self.save()


	def decline(self):
		"""
		Decline a friend request.
		It is 'declined' by setting the 'is_active' field to False
		"""
		self.is_active = False
		self.save()


	def cancel(self):
		"""
		Cancel a friend request
		'cancelled' by setting the 'is_active' field to False.
		This is only different with respect to "declining" through the norification that is generated.
		"""
		self.is_active = False
		self.save()
