from django.urls import path
from .views import GenerateQuoteView, QuoteListView, QuoteDeleteView

urlpatterns = [
    path('generate/', GenerateQuoteView.as_view()),
    path('list/', QuoteListView.as_view()),
    path('delete/<int:pk>/', QuoteDeleteView.as_view()),  # DELETE endpoint
]
