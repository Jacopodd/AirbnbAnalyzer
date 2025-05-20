from pymongo.database import Database
from bson import ObjectId
from datetime import datetime

def crea_recensione(db: Database, recensione: dict):
    result = db["recensioni"].insert_one(recensione)
    print(f"✅ Recensione inserita con ID: {result.inserted_id}")
    return result.inserted_id

def leggi_recensione(db: Database, recensione_id: str):
    return db["recensioni"].find_one({"_id": ObjectId(recensione_id)})

def aggiorna_recensione(db: Database, recensione_id: str, aggiornamenti: dict):
    result = db["recensioni"].update_one(
        {"_id": ObjectId(recensione_id)},
        {"$set": aggiornamenti}
    )
    if result.modified_count > 0:
        print(f"📝 Recensione {recensione_id} aggiornata.")
    else:
        print(f"⚠️ Nessuna recensione aggiornata.")
    return result.modified_count

def elimina_recensione(db: Database, recensione_id: str):
    result = db["recensioni"].delete_one({"_id": ObjectId(recensione_id)})
    if result.deleted_count > 0:
        print(f"🗑️ Recensione {recensione_id} eliminata.")
    else:
        print(f"⚠️ Nessuna recensione eliminata.")
    return result.deleted_count
