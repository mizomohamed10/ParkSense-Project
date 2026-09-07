import json
from datetime import datetime
import paho.mqtt.client as mqtt
from app.config import settings
from app.database import db_parking_spots, db_reservations, db_iot_devices


def handle_qr_entrance(client, payload_str):
    #"check if the QR code is valid and update the reservation status"

    try:
        data = json.loads(payload_str) if payload_str.startswith("{") else {"qr_code": payload_str}
        qr_code = data.get("qr_code")

        print(f"🔍 [Entrance] Checking QR: {qr_code}")
        reservation = db_reservations.get(qr_code)

        if reservation and reservation["status"] == "active":
            reservation["entry_time"] = datetime.now()
            response = {"action": "open", "duration": 5}
            client.publish("parksense/gate/entrance/command", json.dumps(response))
            print(f"🟢 Entrance Approved for QR: {qr_code}")
        else:
            response = {"action": "deny"}
            client.publish("parksense/gate/entrance/command", json.dumps(response))
            print(f"🔴 Entrance Denied for QR: {qr_code}")
    except Exception as e:
        print(f"❌ Error in QR entrance handler: {e}")


def handle_sensor_update(topic, payload_str):
    """تحديث حالة الركنة بناءً على قراءات الـ Ultrasonic"""
    try:
        data = json.loads(payload_str)
        spot_id = data.get("spot_id")
        status = data.get("status")

        if spot_id in db_parking_spots:
            db_parking_spots[spot_id]["status"] = status
            db_parking_spots[spot_id]["distance"] = data.get("distance", 0)
            print(f"📊 Spot {spot_id} updated: {status}")
    except Exception as e:
        print(f"❌ Error in sensor update handler: {e}")


def handle_heartbeat(payload_str):
    """تحديث حالة جهاز الـ ESP32 والـ Uptime"""
    try:
        data = json.loads(payload_str)
        device_id = data.get("device_id")
        db_iot_devices[device_id] = {
            "device_id": device_id,
            "status": "online",
            "uptime": data.get("uptime", 0),
            "last_seen": datetime.now()
        }
        print(f"💓 Heartbeat received from [{device_id}]")
    except Exception as e:
        print(f"❌ Error in heartbeat handler: {e}")        


# Callback عند الاتصال بالـ Broker
def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to Mosquitto Broker on {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}")
    client.subscribe("parksense/parking/+/status")
    client.subscribe("parksense/qr/entrance/scan")
    client.subscribe("parksense/device/+/status")        

# Callback عند وصول أي رسالة
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    
    if topic == "parksense/qr/entrance/scan":
        handle_qr_entrance(client, payload)
    elif "parksense/parking/" in topic:
        handle_sensor_update(topic, payload)
    elif "parksense/device/" in topic:
        handle_heartbeat(payload)

# تجهيز الـ Client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message    


def start_mqtt():
    try:
        mqtt_client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, 60)
        mqtt_client.loop_start()
    except Exception as e:
        print(f"⚠️ Could not connect to MQTT Broker: {e}")