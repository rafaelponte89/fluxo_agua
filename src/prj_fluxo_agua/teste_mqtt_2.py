import paho.mqtt.client as mqtt
from random import randint


broker = 'broker.emqx.io'
port = 1883
topic = "emqx/fluxo_agua"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{randint(0, 100)}'
#username = 'emqx'
#password = 'public'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

vazao_somando = 0   #HERE!

def on_message(client, userdata, msg):
    global vazao_somando
    if msg.topic == topic:
        vazao_somando  += float(msg.payload)   #HERE!
        print(msg.topic+" "+str(msg.payload))
    vazao_somando += vazao_somando
    
client = mqtt.Client(client_id="conexao125")
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)
client.loop_forever()
