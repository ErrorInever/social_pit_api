from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from friend.models import FriendList
from friend.serializers import FriendListSerializer


class FriendListViewSet(ModelViewSet):
	queryset = FriendList.objects.all()
	serializer_class = FriendListSerializer
