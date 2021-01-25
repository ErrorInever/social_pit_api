from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from user.models import CustomUser, Post, UserPostRelation


class CustomUserSerializer(ModelSerializer):
	class Meta:
		model = CustomUser
		fields = '__all__'


class PostSerializer(ModelSerializer):
	annotated_likes = serializers.IntegerField(read_only=True)
	rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)


	class Meta:
		model = Post
		fields = ['id', 'author', 'content', 'title', 'created_on', 'updated_on', 'annotated_likes', 'rating']




class UserPostRelationSerializer(ModelSerializer):
	class Meta:
		model = UserPostRelation
		fields = ('post', 'like', 'rate')