from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
	"""
	Custom user model manager
	"""

	def create_user(self, email, password=None, **extra_fields):
		"""
		Create and save a User
		"""
		if not email:
			raise ValueError(_('The Email must be set'))
		now = timezone.now()
		email = self.normalize_email(email)
		user = self.model(
			email=email, 
			last_login=now, 
			date_joined=now, 
			**extra_fields
			)
		if password:
			user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password, **extra_fields):
		"""
		Create and save a SuperUser
		"""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('Superuser must have is_superuser=True'))
		return self.create_user(email, password, **extra_fields)