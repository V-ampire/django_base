from rest_framework import serializers
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('subscription', 'browser')


class PushMessageSerializer(serializers.Serializer):
    header = serializers.CharField(max_length=64)
    body = serializers.CharField(max_length=128)