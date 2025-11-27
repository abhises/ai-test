from rest_framework import serializers


class QuoteRequestSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=200)
    tone = serializers.CharField(max_length=50, required=False, default="inspirational")