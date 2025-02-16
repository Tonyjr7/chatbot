from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from groq import Groq
from bot.serializers import Payload
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
                    "app_logo": "https://img.freepik.com/free-vector/cartoon-style-robot-vectorart_78370-4103.jpg?t=st=1739712365~exp=1739715965~hmac=0529c037fe9053bd424f85f02362a463e50b32d0e06f43e0380d710d0b9c7d50&w=740",
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
                        "default": "* * * * *",
                    },
                ],
                "target_url": "",
                "tick_url": f"{base_url}/tick",
            }
        }

        return Response(integration_json)

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
            
            telex_format = {
                "message": send_message_to_groq("Hi"),
                "username": "Dream Bot",
                "event_name": "Dream Said",
                "status": "success"
            }

            headers = {"Content-Type": "application/json"}
            if return_url:
                requests.post(return_url, json=telex_format, headers=headers)

            return Response({"status": "success"}, status=202)

        return Response(serializer.errors, status=400)
