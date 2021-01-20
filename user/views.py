from rest_framework.viewsets import ModelViewSet
from user.models import CustomUser
from user.serializers import CustomUserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render


class CustomUserViewSet(ModelViewSet):
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter]
	permission_classes = [IsAuthenticated]
	filter_fields = ['first_name']
	# search_fields = []


def auth(request):
	return render(request, 'oauth.html')

def index(request):
	return render(request, 'index.html')