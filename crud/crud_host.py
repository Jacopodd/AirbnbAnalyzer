from pymongo.database import Database
from bson import ObjectId

def crea_host(db: Database, host: dict):
    result = db["host"].insert_one(host)
    print(f"✅ Host inserito con ID: {result.inserted_id}")
    return result.inserted_id

def leggi_host(db: Database, host_id: str):
    return db["host"].find_one({"_id": host_id})

def aggiorna_host(db: Database, host_id: str, aggiornamenti: dict):
    result = db["host"].update_one(
        {"_id": host_id},
        {"$set": aggiornamenti}
    )
    return result.modified_count

def elimina_host(db: Database, host_id: str):
    result = db["host"].delete_one({"_id": host_id})
    return result.deleted_count

def lista_host(db: Database):
    return list(db["host"].find().sort("nome", 1))
