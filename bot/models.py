from django.db import models

# Create your models here.
class ChatMessage(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_message[:50]} - Bot: {self.bot_response[:50]}"