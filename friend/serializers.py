from rest_framework.serializers import ModelSerializer
from friend.models import FriendList


class FriendListSerializer(ModelSerializer):
	class Meta:
		model = FriendList
		fields = '__all__'