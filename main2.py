import asyncio
from fastapi import FastAPI, WebSocket
import paho.mqtt.client as mqtt

app = FastAPI()
websocket_clients = []
global_loop = None

@app.on_event("startup")
async def startup_event():
    global global_loop
    global_loop = asyncio.get_running_loop()

def on_mqtt_message(client, userdata, msg):
    data = msg.payload.decode()
    for ws in websocket_clients.copy():
        asyncio.run_coroutine_threadsafe(ws.send_text(data), global_loop)

MQTT_BROKER = "localhost"
MQTT_TOPIC = "parking/sensor"

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_mqtt_message
mqtt_client.username_pw_set("admin", "admin")
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        websocket_clients.remove(websocket)

@app.get("/")
async def root():
    return {"message": "Welcome to the Digital Twin API. Use /ws for WebSocket connection."}
