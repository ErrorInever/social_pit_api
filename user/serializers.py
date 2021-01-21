from rest_framework.serializers import ModelSerializer
from user.models import CustomUser, Post


class CustomUserSerializer(ModelSerializer):
	class Meta:
		model = CustomUser
		fields = '__all__'


class PostSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = ['author', 'content', 'title', 'created_on', 'updated_on']
