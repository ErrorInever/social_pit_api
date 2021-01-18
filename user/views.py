from rest_framework.viewsets import ModelViewSet
from user.models import CustomUser
from user.serializers import CustomUserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class CustomUserViewSet(ModelViewSet):
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter]
	filter_fields = ['first_name']
	# search_fields = []