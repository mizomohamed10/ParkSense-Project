from fastapi import APIRouter, HTTPException
from app.database import db_parking_spots, db_reservations

router = APIRouter(prefix="/parking", tags=["Mobile Parking & Reservations"])

@router.get("/spaces")
def get_parking_spaces():
   # """عرض حالة كل الركنات في الوقت الفعلي لتطبيق الموبايل"""
    return {"spaces": list(db_parking_spots.values())}

@router.post("/reserve")
def create_reservation(user_id: int, spot_id: int):
   # """عمل حجز جديد وتوليد QR Code"""
    if spot_id not in db_parking_spots or db_parking_spots[spot_id]["status"] != "available":
        raise HTTPException(status_code=400, detail="Spot is not available")
    
    generated_qr = f"RESERVATION-{user_id}{spot_id}"
    db_reservations[generated_qr] = {
        "user_id": user_id,
        "spot_id": spot_id,
        "status": "active"
    }
    
    return {
        "success": True,
        "message": "Reservation successful",
        "qr_code": generated_qr
    }