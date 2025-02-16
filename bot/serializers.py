from rest_framework import serializers

class Settings(serializers.Serializer):
    label = serializers.CharField()
    type = serializers.CharField()
    required = serializers.BooleanField()
    default = serializers.CharField()

class Payload(serializers.Serializer):
    channel_id = serializers.CharField()
    return_url = serializers.CharField()
    settings = Settings(many=True)

class Message(serializers.Serializer):
    message = serializers.CharField()
