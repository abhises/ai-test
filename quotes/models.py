from django.db import models


class GeneratedQuote(models.Model):
    topic = models.CharField(max_length=200)
    tone = models.CharField(max_length=50)
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return f"{self.topic} - {self.tone}"