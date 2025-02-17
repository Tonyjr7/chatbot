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
                "descriptions": {
                    "app_name": "ChatBot",
                    "app_description": "A chatbot application",
                    "app_logo": "https://img.freepik.com/free-vector/cartoon-style-robot-vectorart_78370-4103.jpg?t=st=1739712365~exp=1739715965~hmac=0529c037fe9053bd424f85f02362a463e50b32d0e06f43e0380d710d0b9c7d50&w=740",
                    "app_url": base_url,
                    "background_color": "#fff",
                },
                "integration_type": "interval",
                "key_features": [
                    "-chatbot"
                ],
                "integration_category": "AI & Machine Learning",
                "settings": [
                    {
                        "label": "message", 
                        "type": "text", 
                        "required": True, 
                        "default": "Hi"
                    },
                    {
                        "label": "interval",
                        "type": "text",
                        "required": True,
                        "default": "* * * * *",
                    }
                ],
                "tick_url": f"{base_url}/tick",
                "target_url": "https://ping.telex.im/v1/webhooks/01951104-c02f-7920-ba4e-31fd5b4d438f"
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
            data = serializer.validated_data
            user_message = data.get("message", "who are you?")  # Use actual message or default
            return_url = data.get("return_url")
            settings = data.get("settings")

            bot_response = send_message_to_groq(user_message)

            telex_format = {
                "message": bot_response,
                "username": "Dream Bot",
                "event_name": "Dream Said",
                "status": "success"
            }

            headers = {"Content-Type": "application/json"}
            if return_url:
                requests.post(return_url, json=telex_format, headers=headers)

            print(request.data)  # Debugging: Print received data
            return Response({"status": "success"}, status=202)

        return Response(serializer.errors, status=400)
