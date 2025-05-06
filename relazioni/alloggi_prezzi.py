# relazioni/alloggi_prezzi.py

from pymongo.database import Database

def esegui_lookup_alloggi_prezzi(db: Database):
    """
    Esegue un'aggregazione $lookup tra alloggi._id e prezzi.id_alloggio (entrambi string).
    Mostra max 5 alloggi, con max 2 prezzi ciascuno.
    """
    pipeline = [
        {
            "$lookup": {
                "from": "prezzi",
                "localField": "_id",
                "foreignField": "id_alloggio",
                "as": "prezzi_giornalieri"
            }
        },
        {
            "$match": {
                "prezzi_giornalieri.0": { "$exists": True }
            }
        },
        {
            "$project": {
                "titolo": 1,
                "prezzi_giornalieri": { "$slice": ["$prezzi_giornalieri", 2] }
            }
        },
        {
            "$limit": 5
        }
    ]

    risultati = db["alloggi"].aggregate(pipeline)

    print("\nRisultati dell'aggregazione alloggi → prezzi:\n")
    for alloggio in risultati:
        print(f"Alloggio: {alloggio.get('titolo', '[senza titolo]')}")
        for p in alloggio["prezzi_giornalieri"]:
            print(f"   ↪ {p.get('data')}: {p.get('prezzo_giornaliero')} €")
        print("-" * 40)

    return "Eseguito con successo"
