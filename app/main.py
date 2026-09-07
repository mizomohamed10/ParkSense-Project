from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.mqtt_handler import start_mqtt, mqtt_client
from app.routers import parking, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 Starting {settings.PROJECT_NAME}...")
    print(f"🌐 Server Local IP for ESP32: {settings.SERVER_LOCAL_IP}")
    start_mqtt()
    yield
    print("🛑 Stopping MQTT Client...")
    mqtt_client.loop_stop()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# تسجيل الـ Routers
app.include_router(parking.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {
        "status": "ParkSense Backend running smoothly!",
        "docs_url": "http://127.0.0.1:8000/docs"
    }