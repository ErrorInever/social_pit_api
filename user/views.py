from rest_framework.viewsets import ModelViewSet
from user.models import CustomUser, Post
from user.serializers import CustomUserSerializer, PostSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from user.permissions import IsAuthorOrStaffOrReadOnly
from django.shortcuts import render


class CustomUserViewSet(ModelViewSet):
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter]
	permission_classes = [IsAuthenticated]
	filter_fields = ['first_name']
	# search_fields = []


class PostViewSet(ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [IsAuthorOrStaffOrReadOnly]

	def perform_create(self, serializer):
		serializer.validated_data['author'] = self.request.user
		serializer.save()


def auth(request):
	return render(request, 'oauth.html')

def index(request):
	return render(request, 'index.html')