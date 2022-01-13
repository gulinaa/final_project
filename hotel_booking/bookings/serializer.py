
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from .models import User
from .models import Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.email')
    receiver = serializers.SlugRelatedField(many=False, slug_field='email', queryset=User.objects.all())

    permission_classes = [IsAuthenticated, ]

    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        print(self.context['request'])
        request = self.context.get('request')
        sender = request.user
        validated_data['sender'] = sender
        return super().create(validated_data)