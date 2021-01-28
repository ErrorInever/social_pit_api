from user.models import UserPostRelation
from django.db.models import Avg


def set_rating(post):
	rating = UserPostRelation.objects.filter(post=post).aggregate(rating=Avg('rate')).get('rating')
	post.rating = rating
	post.save()