from rest_framework.viewsets import ModelViewSet
from user.models import CustomUser
from user.serializers import CustomUserSerializer


class CustomUserViewSet(ModelViewSet):
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserSerializer