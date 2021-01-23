from rest_framework.serializers import ModelSerializer
from user.models import CustomUser, Post, UserPostRelation


class CustomUserSerializer(ModelSerializer):
	class Meta:
		model = CustomUser
		fields = '__all__'


class PostSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = ['id', 'author', 'content', 'title', 'created_on', 'updated_on']


class UserPostRelationSerializer(ModelSerializer):
	class Meta:
		model = UserPostRelation
		fields = ('post', 'like', 'rate')