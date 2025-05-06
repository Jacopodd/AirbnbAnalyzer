# relazioni/host_alloggi_lookup.py

from pymongo.database import Database

def esegui_lookup_host_alloggi(db: Database):
    """
    Esegue un'aggregazione $lookup tra host.id e alloggi.host_id.
    Mostra i primi host con almeno un alloggio associato.
    """
    pipeline = [
        {
            "$lookup": {
                "from": "alloggi",
                "localField": "_id",  # campo esplicito, come da tua shell
                "foreignField": "host_id",
                "as": "alloggi_gestiti"
            }
        }
    ]

    risultati = db["host"].aggregate(pipeline)

    print("\nRisultati dell'aggregazione host → alloggi:\n")
    count = 0
    for host in risultati:
        num_alloggi = len(host.get("alloggi_gestiti", []))
        print(f"Host ID: {host.get('_id')} - Nome: {host.get('nome')} - Alloggi trovati: {num_alloggi}")
        if num_alloggi > 0:
            for alloggio in host["alloggi_gestiti"][:3]:  # max 3 per host
                print(f"   ↪ Alloggio: {alloggio.get('titolo', '[senza titolo]')}")
        print("-" * 40)
        count += 1
        if count >= 5:
            break

    return risultati.__sizeof__()