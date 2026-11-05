from rest_framework import serializers
from .models import Dht11

class DHT11serialize(serializers.ModelSerializer):
    class Meta:
        model = Dht11
        fields = ["id", "temperature", "humidity", "date"]
        read_only_fields = ["id", "date"]
