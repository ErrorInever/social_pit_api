import dotenv
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from cloudinary.models import CloudinaryField


class CustomUser(AbstractUser):
	username = None
	email = models.EmailField(_('email address'), unique=True)
	first_name = models.CharField(max_length=15)
	last_name = models.CharField(max_length=15)
	birthday = models.DateField(auto_now_add=True)
	hometown = models.CharField(max_length=25)
	bio = models.CharField(max_length=100, blank=True)
	profile_picture = CloudinaryField('image', null=True, blank=True, default="logo.png")
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	def __str__(self):
		return self.email


class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	content = models.TextField()
	title = models.CharField(max_length=15)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

