from pymongo.database import Database
from bson import ObjectId
from datetime import datetime

def crea_prezzo(db: Database, prezzo: dict):
    result = db["prezzi"].insert_one(prezzo)
    print(f"✅ Prezzo inserito con ID: {result.inserted_id}")
    return result.inserted_id

def leggi_prezzo(db: Database, prezzo_id: str):
    return db["prezzi"].find_one({"_id": ObjectId(prezzo_id)})

def aggiorna_prezzo(db: Database, prezzo_id: str, aggiornamenti: dict):
    result = db["prezzi"].update_one(
        {"_id": ObjectId(prezzo_id)},
        {"$set": aggiornamenti}
    )
    return result.modified_count

def elimina_prezzo(db: Database, prezzo_id: str):
    result = db["prezzi"].delete_one({"_id": ObjectId(prezzo_id)})
    return result.deleted_count
