# crud_alloggi.py

from pymongo.database import Database
from bson import ObjectId
from datetime import datetime


def crea_alloggio(db: Database, alloggio: dict):
    """
    Inserisce un nuovo alloggio nella collezione 'alloggi'.
    """
    result = db["alloggi"].insert_one(alloggio)
    print(f"✅ Alloggio inserito con ID: {result.inserted_id}")
    print("🧪 Documento inserito:", db["alloggi"].find_one({"_id": result.inserted_id}))
    return alloggio["_id"]


def leggi_alloggi(db: Database, filtro: dict = {}, limite: int = 10):
    """
    Legge gli alloggi in base a un filtro opzionale.
    """
    risultati = list(db["alloggi"].find(filtro).limit(limite))
    print(f"🔍 Trovati {len(risultati)} alloggi:")
    for alloggio in risultati:
        print(f"- {alloggio.get('titolo', '[senza titolo]')} (ID: {alloggio.get('_id')})")
    return risultati


def aggiorna_alloggio(db: Database, alloggio_id: str, aggiornamenti: dict):
    """
    Aggiorna un alloggio esistente dato il suo _id e un dizionario di aggiornamenti.
    """
    try:
        filtro = {"_id": ObjectId(alloggio_id)}
    except Exception:
        print("❌ ID non valido")
        return 0

    result = db["alloggi"].update_one(filtro, {"$set": aggiornamenti})

    if result.modified_count > 0:
        print(f"🛠️ Alloggio {alloggio_id} aggiornato.")
    else:
        print(f"⚠️ Nessun alloggio aggiornato.")
    return result.modified_count



def elimina_alloggio(db: Database, alloggio_id: str):
    """
    Elimina un alloggio dalla collezione 'alloggi' dato il suo _id.
    """
    result = db["alloggi"].delete_one({"_id": alloggio_id})
    if result.deleted_count > 0:
        print(f"🗑️ Alloggio {alloggio_id} eliminato.")
    else:
        print(f"⚠️ Nessun alloggio eliminato.")
    return result.deleted_count
