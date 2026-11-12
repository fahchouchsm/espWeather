from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import telebot

@api_view(['GET'])
def Dlist(request):
    all_data = Dht11.objects.all()
    data = DHT11serialize(all_data, many=True).data
    return Response({'data': data})

class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize

    def perform_create(self, serializer):
        data = serializer.save()
        temperature = data.temperature
        if temperature > 25:
            message = f"Alerte ! Temperature = {temperature} °C"
            send_mail(
                subject="Alerte Temperature",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_ALERT_RECIPIENT],
                fail_silently=False
            )
            telegram_token = getattr(settings, 'TELEGRAM_TOKEN', None)
            telegram_chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
            if telegram_token and telegram_token != "TOKEN_DU_BOT" and telegram_chat_id:
                try:
                    bot = telebot.TeleBot(telegram_token)
                    bot.send_message(telegram_chat_id, message)
                except Exception as e:
                    print(f"Erreur envoi Telegram: {e}")
