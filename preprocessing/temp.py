def debug_coordinate_su_uno(db):
    alloggio = db["alloggi"].find_one()
    _id = alloggio["_id"]
    coord_str = alloggio.get("coordinate")

    print(f"ID: {_id}")
    print(f"RAW: {repr(coord_str)}")  # <-- mostra caratteri invisibili
    print(f"Tipo: {type(coord_str)}")

    try:
        lat_str, lon_str = coord_str.strip().split(",")
        lat = float(lat_str.strip())
        lon = float(lon_str.strip())
    except Exception as e:
        print(f"❌ Parsing fallito: {e}")
        return

    location = {
        "type": "Point",
        "coordinates": [lon, lat]
    }

    result = db["alloggi"].update_one(
        {"_id": _id},
        {"$set": {"location": location}}
    )

    print("✅ Aggiornati:", result.modified_count)
    print("📦 Nuovo campo location:", db["alloggi"].find_one({"_id": _id}).get("location"))
