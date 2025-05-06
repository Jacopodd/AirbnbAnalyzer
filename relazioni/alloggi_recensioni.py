# relazioni/alloggi_recensioni_lookup.py

from pymongo.database import Database

def esegui_lookup_alloggi_recensioni(db: Database):
    """
    Esegue un'aggregazione $lookup tra alloggi.id e recensioni.id_alloggio.
    Mostra i primi alloggi con almeno una recensione.
    """
    pipeline = [
        {
            "$lookup": {
                "from": "recensioni",
                "localField": "_id",
                "foreignField": "id_alloggio",
                "as": "recensioni_alloggio"
            }
        }
    ]

    risultati = db["alloggi"].aggregate(pipeline)

    print("\nRisultati dell'aggregazione alloggi → recensioni:\n")
    count = 0
    for alloggio in risultati:
        num_recensioni = len(alloggio.get("recensioni_alloggio", []))
        print(f"Alloggio: {alloggio.get('titolo', '[senza titolo]')} - Recensioni trovate: {num_recensioni}")
        if num_recensioni > 0:
            for rec in alloggio["recensioni_alloggio"][:2]:  # max 2 per alloggio
                print(f"   ↪ {rec.get('utente')}: {rec.get('testo', '[nessun commento]')[:50]}...")
        print("-" * 40)
        count += 1
        if count >= 5:
            break

    return risultati.__sizeof__()
