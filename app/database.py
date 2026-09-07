from datetime import datetime, timedelta

#spots status: available, occupied, reserved
db_parking_spots = {
    1: {"spot_id": 1, "code": "A-01", "status": "available", "distance": 150},
    2: {"spot_id": 2, "code": "A-02", "status": "available", "distance": 160},
}

#available reservations
now = datetime.now()
db_reservations = {
    "RESERVATION-839201": {
        "user_id": 15,
        "spot_id": 1,
        "status": "active",
        "start_time": now - timedelta(minutes=10),
        "end_time": now + timedelta(hours=2),
        "entry_time": None,
        "exit_time": None,
        "price_per_hour": 20.0
    }
}


db_iot_devices = {}