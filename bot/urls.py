from django.urls import path
from bot.views import IntegrationView, MessageView

urlpatterns = [
    path('integration-json', IntegrationView.as_view(), name='webhook'),
    path('tick', MessageView.as_view(), name='tick'),
]