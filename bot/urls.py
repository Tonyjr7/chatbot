from django.urls import path
from bot.views import IntegrationView, MessageView, ReceiveMessage

urlpatterns = [
    path('integration-json', IntegrationView.as_view(), name='webhook'),
    path('tick', MessageView.as_view(), name='tick'),
    path('target', ReceiveMessage.as_view(), name='target'),
]