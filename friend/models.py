from django.db import models
from django.conf import settings
from django.utils import timezone


class FriendList(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
	friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')

	def __str__(self):
		return f'{self.user.first_name}{self.user.first_name}'

	def add_friend(self, account):
		"""
		Add a new friend
		"""
		if not account in self.friends.all():
			self.friends.add(account)

	def remove_friend(self, account):
		"""
		Remove a friend
		"""
		if account in self.friends.all():
			self.friends.remove(account)

	def unfriend(self, removee):
		"""
		Initiate the action of unfriending someone.
		"""
		remover_friends_list = self # person terminating the friendship

		# Remove frined from remover friend list
		remover_friends_list.remove_friend(removee)

		# Remove frined from removee friend list
		friends_list = FriendList.objects.get(user=removee)
		friends_list.remove_friend(self.user)

	def is_mutual_friend(self, friend):
		"""
		Is this a friend?
		"""
		if friend in self.friends.all():
			return True
		else:
			return False
