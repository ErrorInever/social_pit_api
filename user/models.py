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
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_posts')
	content = models.TextField()
	title = models.CharField(max_length=15)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	readers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserPostRelation', related_name='posts')
	rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)

	def __str__(self):
		return self.title


class UserPostRelation(models.Model):
	RATE_CHOICES = (
		(1, 'Very bad'),
		(2, 'Bad'),
		(3, 'Normal'),
		(4, 'Good'),
		(5, 'Amazing')
	)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	like = models.BooleanField(default=False)
	rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

	def __str__(self):
		return f'{self.user.first_name}{self.user.first_name}: {self.post}, RATE {self.rate}'