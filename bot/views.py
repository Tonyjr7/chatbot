from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from groq import Groq
from bot.serializers import Payload, Message
from bot.models import ChatMessage  # Assuming you have a model for storing messages
import requests
import os

class IntegrationView(APIView):
    def get(self, request):
        base_url = request.build_absolute_uri('/')[:-1]

        integration_json = {
            "data": {
                "date": {"created_at": "2025-02-09", "updated_at": "2025-02-09"},
                "descriptions": {
                    "app_name": "Groq ChatBot",
                    "app_description": "A chatbot application",
                    "app_logo": "https://img.freepik.com/free-vector/cartoon-style-robot-vectorart_78370-4103.jpg",
                    "app_url": base_url,
                    "background_color": "#fff",
                },
                "is_active": False,
                "integration_type": "interval",
                "key_features": ["-chatbot", "-ask it anything"],
                "integration_category": "AI & Machine Learning",
                "author": "Anthony Triumph",
                "website": base_url,
                "settings": [
                    {
                        "label": "interval",
                        "type": "text",
                        "required": True,
                        "default": "*/5 * * * *",
                    },
                ],
                "target_url": f"{base_url}/target",
                "tick_url": f"{base_url}/tick"
            }
        }

        return Response(integration_json)

class ReceiveMessage(APIView):
    def post(self, request):
        serializer = Message(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data.get("message")
            chatbot_response = send_message_to_groq(message)  
            
            chat_entry = ChatMessage.objects.create(user_message=message, bot_response=chatbot_response)
            
            return Response({"status": "received", "message_id": chat_entry.id}, status=200)
        
        return Response(serializer.errors, status=400)

def send_message_to_groq(message):
    key = os.getenv("API_KEY")
    if not key:
        return "API key is missing"

    client = Groq(api_key=key)
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": message}],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

class MessageView(APIView):
    def post(self, request):
        serializer = Payload(data=request.data)
        if serializer.is_valid():
            return_url = serializer.validated_data.get("return_url")
            message_id = serializer.validated_data.get("message_id")
            
            try:
                chat_entry = ChatMessage.objects.get(id=message_id)
                chatbot_response = chat_entry.bot_response
            except ChatMessage.DoesNotExist:
                return Response({"error": "Message not found"}, status=404)
            
            telex_format = {
                "message": chatbot_response,  # Use stored chatbot response
                "username": "Dream Bot",
                "event_name": "Dream Said",
                "status": "success"
            }

            headers = {"Content-Type": "application/json"}
            if return_url:
                requests.post(return_url, json=telex_format, headers=headers)

            return Response({"status": "success"}, status=202)

        return Response(serializer.errors, status=400)
