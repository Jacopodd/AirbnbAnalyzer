# main.py

from pymongo import MongoClient
from relazioni.host_alloggi import esegui_lookup_host_alloggi
from relazioni.alloggi_recensioni import esegui_lookup_alloggi_recensioni
from relazioni.alloggi_prezzi import esegui_lookup_alloggi_prezzi
from relazioni.alloggi_quartieri import esegui_lookup_alloggi_quartieri

# scripts/aggiorna_location_alloggi.py

def aggiorna_location_alloggi(db):
    """
    Aggiorna tutti i documenti nella collezione 'alloggi', convertendo il campo 'coordinate'
    (es. '45.44806,9.17373') in un oggetto GeoJSON 'location'.
    """
    print("🚀 Avvio aggiornamento campo 'location' in GeoJSON...")
    alloggi = db["alloggi"].find()
    count_success = 0
    count_error = 0

    for alloggio in alloggi:
        _id = alloggio["_id"]
        coord_str = alloggio.get("coordinate")

        if not coord_str or "location" in alloggio:
            continue

        try:
            lat_str, lon_str = coord_str.strip().split(",")
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
        except Exception as e:
            print(f"❌ Errore parsing per alloggio {_id}: {e}")
            count_error += 1
            continue

        geojson = {
            "type": "Point",
            "coordinates": [lon, lat]  # GeoJSON: [LONG, LAT]
        }

        result = db["alloggi"].update_one(
            {"_id": _id},
            {"$set": {"location": geojson}}
        )

        if result.modified_count > 0:
            count_success += 1

    print(f"\n✅ Aggiornamento completato.")
    print(f"📌 Alloggi aggiornati: {count_success}")
    print(f"⚠️ Errori di parsing: {count_error}")



def main():
    # client = MongoClient("mongodb://localhost:27017")
    # db = client["airbnbMilano"]
    #
    #
    # print("=== ESECUZIONE JOIN PREZZI → ALLOGGI ===")
    # # print(db["prezzi"].count_documents({"id_alloggio": "23986"}))  # quante righe ci sono?
    # # print(db["prezzi"].find_one({"id_alloggio": "23986"}))  # verifica che sia accessibile
    # #print(list(db["prezzi"].index_information()))
    # print(db["alloggi"].count_documents({"location": {"$exists": True}}))
    #
    # #esegui_lookup_host_alloggi(db)
    # #esegui_lookup_alloggi_recensioni(db)
    # #esegui_lookup_alloggi_prezzi(db)
    # esegui_lookup_alloggi_quartieri(db)
    # print("=== FINE ===")
    import os

    print("Contenuto della cartella static:")
    print(os.listdir(os.path.join(os.path.dirname(__file__), "static")))


if __name__ == "__main__":
    main()
