from fastapi import APIRouter
from datetime import datetime
from app.database import db_parking_spots, db_iot_devices

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

@router.get("/dashboard-summary")
def get_admin_dashboard_summary():
    #"""تجميع إحصائيات لوحة التحكم وحالة أجهزة الـ IoT"""
    total_spots = len(db_parking_spots)
    occupied = sum(1 for s in db_parking_spots.values() if s["status"] == "occupied")
    available = sum(1 for s in db_parking_spots.values() if s["status"] == "available")

    now = datetime.now()
    devices_summary = []
    
    for dev_id, dev_info in db_iot_devices.items():
        time_diff = (now - dev_info["last_seen"]).total_seconds()
        is_online = time_diff <= 30
        
        devices_summary.append({
            "device_id": dev_id,
            "status": "Online" if is_online else "Offline",
            "last_seen_seconds_ago": int(time_diff)
        })

    return {
        "parking_summary": {
            "total": total_spots,
            "available": available,
            "occupied": occupied
        },
        "iot_devices": devices_summary,
        "parking_map": list(db_parking_spots.values())
    }