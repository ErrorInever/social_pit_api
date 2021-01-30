from django.db import IntegrityError


class AlreadyFriendsError(IntegrityError):
    pass


class FriendListsDoesNotExist(IntegrityError):
	pass
