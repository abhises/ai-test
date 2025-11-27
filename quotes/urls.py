from django.urls import path
from .views import GenerateQuoteView, QuoteListView


urlpatterns = [
path('generate/', GenerateQuoteView.as_view()),
path('list/', QuoteListView.as_view()),
]