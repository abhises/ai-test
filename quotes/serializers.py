from rest_framework import serializers
from .models import GeneratedQuote


class QuoteRequestSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=200)
    tone = serializers.CharField(max_length=50, required=False, default="inspirational")


class GeneratedQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedQuote
        fields = ["id", "topic", "tone", "quote", "created_at"]