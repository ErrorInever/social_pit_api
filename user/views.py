from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from user.models import CustomUser, Post, UserPostRelation
from user.serializers import CustomUserSerializer, PostSerializer, UserPostRelationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from user.permissions import IsAuthorOrStaffOrReadOnly
from django.shortcuts import render
from django.db.models import Count, Case, When, Avg


class CustomUserViewSet(ModelViewSet):
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter]
	permission_classes = [IsAuthenticated]
	filter_fields = ['first_name']
	# search_fields = []


class PostViewSet(ModelViewSet):
	queryset = Post.objects.all().annotate(
		annotated_likes=Count(Case(When(userpostrelation__like=True, then=1))),
		rating=Avg('userpostrelation__rate')
		).select_related('author')
	serializer_class = PostSerializer
	permission_classes = [IsAuthorOrStaffOrReadOnly]

	def perform_create(self, serializer):
		serializer.validated_data['author'] = self.request.user
		serializer.save()


class UserPostRelationView(UpdateModelMixin, GenericViewSet):
	permission_classes = [IsAuthenticated]
	queryset = UserPostRelation.objects.all()
	serializer_class = UserPostRelationSerializer
	lookup_field = 'post'

	def get_object(self):
		"""Access through current post_id and user id from request. We don't transfer relation id in url"""
		obj, _ = UserPostRelation.objects.get_or_create(user=self.request.user, post_id=self.kwargs['post'])
		return obj


def auth(request):
	return render(request, 'oauth.html')

def index(request):
	return render(request, 'index.html')