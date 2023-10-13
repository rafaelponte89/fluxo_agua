def on_message(mqtt_client, userdata, msg):
   print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')