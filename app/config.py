import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class Settings:
    PROJECT_NAME: str = "ParkSense Engine"

    # إعدادات الـ MQTT Broker (Mosquitto)
    MQTT_BROKER_HOST: str = "localhost"  # أو ضع الـ Local IP لـ Mosquitto
    MQTT_BROKER_PORT: int = 1883
    
    # الـ Local IP بتاع جهازك لطباعته عند بداية التشغيل (عشان عمر يكتبه في الـ ESP32)
    SERVER_LOCAL_IP: str = get_local_ip()

settings = Settings()