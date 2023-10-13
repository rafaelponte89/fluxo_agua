from django.conf import settings
import paho.mqtt.client as mqtt
from .views import salvar_fluxo
from random import random
from time import sleep
# Create your views here.

def on_message(mqtt_client, userdata, msg):
   print((msg.payload).decode('utf-8'))
   msg_fluxo = (msg.payload).decode('utf-8')
   salvar_fluxo(float(msg_fluxo))

def on_connect(mqtt_client, userdata, flags, rc):
   if rc == 0:
       print('Sucesso na conexão com o Broker')
       mqtt_client.subscribe('emqx/fluxo_agua')
   else:
       print('Erro na conexão... Code:', rc)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)

client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)


