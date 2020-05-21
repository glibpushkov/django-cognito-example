from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Used to retrieve user info """

    class Meta:
        model = User
        fields = '__all__'
