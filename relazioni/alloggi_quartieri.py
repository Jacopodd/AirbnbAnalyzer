from pymongo.database import Database

def esegui_lookup_alloggi_quartieri(db: Database):
    """
    Esegue $geoIntersects tra location degli alloggi e poligoni dei quartieri.
    Mostra i primi 5 alloggi con quartiere identificato.
    """
    print("\nRisultati dell'aggregazione alloggi → quartieri (geospaziale):\n")
    count = 0
    aggiornati = 0

    for alloggio in db["alloggi"].find():
        location = alloggio.get("location")
        if not location:
            continue

        quartiere = db["quartieri"].find_one({
            "geometry": {
                "$geoIntersects": {
                    "$geometry": location
                }
            }
        })

        nome_quartiere = (
            quartiere.get("properties", {}).get("quartiere")
            if quartiere else None
        )

        print(f"Alloggio: {alloggio.get('titolo', '[senza titolo]')}")
        print(f" - Coordinate: {location}")
        if nome_quartiere:
            print(f"   ✅ Quartiere trovato: {nome_quartiere}")
            aggiornati += 1
        else:
            print("   ❌ Nessun quartiere corrispondente.")
        print("-" * 40)

        count += 1
        if count >= 5:
            break

    print(f"\nTotale alloggi con quartiere identificato (in questa anteprima): {aggiornati}")
